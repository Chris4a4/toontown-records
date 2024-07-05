from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder
from api.logging.logging import audit_log

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
from api.records.records import lookup_record_info
from api.accounts.router import get_all_users

from json import dumps, loads

from time import time
from datetime import datetime

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


class Submission(BaseModel):
    record_name: str
    usernames: List[str]
    value_score: int | None = None
    value_time: str | None = None
    evidence: str


@submissions_router.post('/api/submissions/submit', tags=['Logged'])
async def submit(data: Submission, audit_id: int):
    new_submission = data.model_dump()

    new_submission['submitter_id'] = audit_id
    new_submission['timestamp'] = int(time())
    new_submission['status'] = 'PENDING'

    usernames = new_submission['usernames']  # Get rid of username field and replace with user_ids in the database doc
    new_submission['user_ids'] = []
    del new_submission['usernames']

    # Lookup record
    record = lookup_record_info(new_submission['record_name'])
    if not record:
        return {
            'success': False,
            'message': 'Could not find a record with that name'
        }
    
    # Check users
    username_to_id = (await get_all_users())['data']

    max_players = record['max_players']
    if len(usernames) > max_players:
        return {
            'success': False,
            'message': f'Max of {max_players} users for this record'
        }

    for username in usernames:
        if username in username_to_id:
            new_submission['user_ids'].append(username_to_id[username])
        else:
            return {
                'success': False,
                'message': f'Could not find user: {username}'
            }
    
    # Check values/time
    submitted_time = new_submission['value_time'] is not None
    submitted_score = new_submission['value_score'] is not None
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
    
    if time_required:
        try:
            new_submission['value_time'] = to_ms(new_submission['value_time'])  # Convert from string to int
        except ValueError:
            return {
                'success': False,
                'message': 'Invalid time format provided. Accepted formats are (milleseconds optional): H:M:S, M:S, S'
            }
        
        if new_submission['value_time'] <= 0:
            return {
                'success': False,
                'message': 'Time must be positive'
            }

    if score_required and new_submission['value_score'] < 0:
        return {
            'success': False,
            'message': 'Score cannot be negative'
        }

    result = Mongo_Config.submissions.insert_one(new_submission)

    audit_log('submit', str(result.inserted_id), audit_id)
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


# Intentionally light on error handling since it's always going to be a mod-only command and should be flexible
@submissions_router.post('/api/submissions/edit/{submission_id}', tags=['Logged'])
async def edit_submission(submission_id: str, data: EditSubmission, audit_id: int):
    edit_data = data.model_dump()

    to_edit = {}
    for key, value in edit_data.items():
        if value is not None:
            to_edit[key] = value

    query = {'_id': ObjectId(submission_id)}
    update = {'$set': to_edit}

    result = Mongo_Config.submissions.update_one(query, update)

    if result:
        audit_log('edit_submission', submission_id, audit_id, additional_info=to_edit)
        return {
            'success': True,
            'message': 'Successfully editted submission'
        }

    return {
        'success': False,
        'message': 'Could not find a submission with that ID'
    }


@submissions_router.get('/api/submissions/approve/{submission_id}', tags=['Logged'])
async def approve_submission(submission_id: str, audit_id: int):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'APPROVED'}}

    result = Mongo_Config.submissions.update_one(query, update)

    if result:
        audit_log('approve_submission', submission_id, audit_id)
        return {
            'success': True,
            'message': 'Successfully approved submission'
        }
    
    return {
        'success': False,
        'message': f'Could not find a submission with that ID'
    }


@submissions_router.get('/api/submissions/deny/{submission_id}', tags=['Logged'])
async def deny_submission(submission_id: str, audit_id: int):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'DENIED'}}

    result = Mongo_Config.submissions.update_one(query, update)

    if result:
        audit_log('deny_submission', submission_id, audit_id)
        return {
            'success': True,
            'message': 'Successfully denied submission'
        }

    return {
        'success': False,
        'message': f'Could not find a submission with that ID'
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


@submissions_router.get('/api/submissions/get_submissions/{user_id}', tags=['Unlogged'])
async def get_submissions(user_id: int):
    query = {'user_ids': user_id}

    documents = Mongo_Config.submissions.find(query)
    if not documents:
        return {
            'success': False,
            'message': 'User not found',
            'data': []
        }

    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return {
        'success': True,
        'message': 'Got all submissions featuring user',
        'data': to_json
    }

