from api.config.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder
from api.logging.logging import audit_log

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
from api.records.records import lookup_record_info
from api.accounts.router import get_all_users
from bson.errors import InvalidId
from api.config.config import Config

from json import dumps, loads

from time import time
from datetime import datetime

from api.logging.webhooks import send_webhook

submissions_router = APIRouter()


# Converts a time string into seconds
# Throws a ValueError if the string is strangely formatted
def to_ms(value_string):
    if '.' not in value_string:
        value_string += '.0'

    # Check inputted text against all valid formats
    valid_formats = ['%H:%M:%S.%f', '%M:%S.%f', '%S.%f']
    for test_format in valid_formats:
        try:
            dt = datetime.strptime(value_string, test_format)
            return int(dt.hour * 3600000 + dt.minute * 60000 + dt.second * 1000 + dt.microsecond / 1000)
        except ValueError:
            pass

    # Unknown format
    raise ValueError


# Validates a full submission object, with user IDs
def validate_submission(submission, username_to_id):
    # Check evidence
    evidence = submission['evidence']
    if len(evidence) > 100:
        return {
            'success': False,
            'message': 'Evidence must be 100 characters or less'
        }

    if not evidence.startswith('https://'):
        return {
            'success': False,
            'message': 'Evidence must start with "https://"'
        }
    
    VALID_STARTS = ['https://www.youtube.com/', 'https://www.youtu.be/', 'https://youtube.com/', 'https://youtu.be/']
    for start in VALID_STARTS:
        if evidence.startswith(start):
            break
    else:
        return {
            'success': False,
            'message': 'Evidence must be a YouTube link'
        }
    
    if '|' in evidence:  # | is a special character in the webhooks
        return {
            'success': False,
            'message': 'Evidence must be a valid YouTube link'
        }

    # Lookup record
    record = lookup_record_info(submission['record_name'])
    if not record:
        return {
            'success': False,
            'message': 'Could not find a record with that name'
        }
    
    # Check users
    max_players = record['max_players']
    user_ids = submission['user_ids']
    if len(user_ids) > max_players:
        return {
            'success': False,
            'message': f'Max of {max_players} users for this record'
        }
    
    if len(user_ids) == 0:
        return {
            'success': False,
            'message': 'Need to add at least one user'
        }

    if len(user_ids) != len(set(user_ids)):
        return {
            'success': False,
            'message': 'Each user can only be added once'
        }
    
    id_to_username = {v: k for k, v in username_to_id.items()}
    for id in user_ids:
        if id not in id_to_username:
            return {
                'success': False,
                'message': f'Could not find user id: {id[:Config.MAX_NAME_LEN]}'
            }

    # Check values/time
    submitted_time = submission['value_time'] is not None
    submitted_score = submission['value_score'] is not None
    score_required = record['score_required']
    time_required = record['time_required']

    if score_required and not submitted_score:
        return {
            'success': False,
            'message': 'This record requires a score'
        }
    
    if submitted_score and not score_required:
        return {
            'success': False,
            'message': 'You cannot submit a score for this record'
        }

    if time_required and not submitted_time:
        return {
            'success': False,
            'message': 'This record requires a time'
        }

    if submitted_time and not time_required:
        return {
            'success': False,
            'message': 'You cannot submit a time for this record'
        }
    
    if submitted_time and submission['value_time'] <= 0:
        return {
            'success': False,
            'message': 'Time must be positive'
        }
    
    if submitted_time and submission['value_time'] >= 60 * 60 * 1000:
        return {
            'success': False,
            'message': 'Time must be less than 10 hours'
        }

    if submitted_score and submission['value_score'] < 0:
        return {
            'success': False,
            'message': 'Score cannot be negative'
        }

    if submitted_score and submission['value_score'] >= 10000:
        return {
            'success': False,
            'message': 'Score must be less than 10000'
        }
    
    return {
        'success': True,
        'message': 'Validated submission'
    }


class Submission(BaseModel):
    record_name: str
    usernames: List[str]
    value_score: int | None = None
    value_time: str | None = None
    evidence: str


@submissions_router.post('/api/submissions/submit', tags=['Logged'])
async def submit(data: Submission, audit_id: int):
    new_submission = data.model_dump()

    new_submission['user_ids'] = []
    new_submission['submitter_id'] = audit_id
    new_submission['timestamp'] = int(time())
    new_submission['status'] = 'PENDING'

    # Get rid of username field and replace with user_ids in the database doc
    usernames = new_submission['usernames']
    del new_submission['usernames']

    username_to_id = (await get_all_users())['data']
    for username in usernames:
        if username in username_to_id:
            new_submission['user_ids'].append(username_to_id[username])
        else:
            return {
                'success': False,
                'message': f'Could not find user: {username[:Config.MAX_NAME_LEN]}'
            }

    # Convert time if it was given
    if new_submission['value_time']:
        try:
            new_submission['value_time'] = to_ms(new_submission['value_time'])  # Convert from string to int
        except ValueError:
            return {
                'success': False,
                'message': 'Invalid time format provided. Accepted formats are (milleseconds optional): H:M:S, M:S, S'
            }

    # Check validation result
    validation_result = validate_submission(new_submission, username_to_id)
    if not validation_result['success']:
        return validation_result

    # Write to database
    result = Mongo_Config.submissions.insert_one(new_submission)

    audit_log('submit', str(result.inserted_id), audit_id)
    send_webhook('submit', audit_id, new_submission)
    return {
        'success': True,
        'message': 'Submission created successfully'
    }


class EditSubmission(BaseModel):
    record_name: str | None = None
    user_ids: List[int] | None = None
    value_score: int | None = None
    value_time: int | None = None
    evidence: str | None = None


@submissions_router.post('/api/submissions/edit/{submission_id}', tags=['Logged'])
async def edit_submission(submission_id: str, data: EditSubmission, audit_id: int):
    try:
        original_submission = Mongo_Config.submissions.find_one({'_id': ObjectId(submission_id)})
    except InvalidId:
        return {
            'success': False,
            'message': 'Not a valid ID'
        }

    if not original_submission:
        return {
            'success': False,
            'message': 'Could not find a submission with that ID'
        }

    # Determine what the record will look like after edits
    editted_submission = loads(dumps(original_submission, cls=MongoJSONEncoder))
    edit_data = data.model_dump()

    to_edit = {}
    for key, value in edit_data.items():
        if value is not None:
            to_edit[key] = value
            editted_submission[key] = value

    # Check validation result
    username_to_id = (await get_all_users())['data']
    validation_result = validate_submission(editted_submission, username_to_id)
    if not validation_result['success']:
        return validation_result

    # Attempt to write to database
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': to_edit}

    result = Mongo_Config.submissions.update_one(query, update)
    if not result:
        return {
            'success': False,
            'message': 'Could not find a submission with that ID'
        }
    
    audit_log('edit_submission', submission_id, audit_id, additional_info=to_edit)
    send_webhook('edit_submission', audit_id, editted_submission)
    return {
        'success': True,
        'message': 'Successfully editted submission'
    }


@submissions_router.get('/api/submissions/approve/{submission_id}', tags=['Logged'])
async def approve_submission(submission_id: str, audit_id: int):
    try:
        query = {
            '_id': ObjectId(submission_id),
            'status': {'$in': ['PENDING', 'APPROVED']}
        }
    except InvalidId:
        return {
            'success': False,
            'message': 'Not a valid ID'
        }
    
    submission = Mongo_Config.submissions.find_one(query)
    if not submission:
        return {
            'success': False,
            'message': 'Could not find a pending or denied submission with that ID'
        }

    update = {'$set': {'status': 'APPROVED'}}
    Mongo_Config.submissions.update_one(query, update)

    audit_log('approve_submission', submission_id, audit_id)
    send_webhook('approve_submission', audit_id, submission)
    return {
        'success': True,
        'message': 'Successfully approved submission'
    }


@submissions_router.get('/api/submissions/deny/{submission_id}', tags=['Logged'])
async def deny_submission(submission_id: str, audit_id: int):
    try:
        query = {
            '_id': ObjectId(submission_id),
            'status': {'$in': ['PENDING', 'APPROVED']}
        }
    except InvalidId:
        return {
            'success': False,
            'message': 'Not a valid ID'
        }

    submission = Mongo_Config.submissions.find_one(query)
    if not submission:
        return {
            'success': False,
            'message': 'Could not find a pending or approved submission with that ID'
        }

    update = {'$set': {'status': 'DENIED'}}
    Mongo_Config.submissions.update_one(query, update)

    audit_log('deny_submission', submission_id, audit_id)
    send_webhook('deny_submission', audit_id, submission)
    return {
        'success': True,
        'message': 'Successfully denied submission'
    }


@submissions_router.get('/api/submissions/get_pending', tags=['Unlogged'])
async def get_pending_submissions():
    query = {'status': 'PENDING'}

    documents = Mongo_Config.submissions.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return {
        'success': True,
        'message': 'Got all pending submissions',
        'data': to_json
    }
