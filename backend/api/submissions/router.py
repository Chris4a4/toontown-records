from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder
from api.logging.logging import audit_log

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId

from json import dumps, loads

from time import time

submissions_router = APIRouter()


class Submission(BaseModel):
    record_name: str
    submitter_id: int
    user_ids: List[int]
    value_score: int | None = None
    value_time: int | None = None
    evidence: str


# TODO error handling
# TODO handle wrong inputs
# TODO use audit id instead of submitter and rename date to timestamp
@submissions_router.post('/api/submissions/submit', tags=['Logged'])
async def submit_record(data: Submission, audit_id: int):
    new_submission = data.model_dump()

    #new_submission['submitter_id'] = 
    new_submission['date'] = int(time())
    new_submission['status'] = 'PENDING'

    result = Mongo_Config.submissions.insert_one(new_submission)

    audit_log('submit_record', str(result.inserted_id), audit_id)
    return {'status:': 'success'}


class EditSubmission(BaseModel):
    record_name: str | None = None
    user_ids: List[int] | None = None
    value_score: int | None = None
    value_time: int | None = None
    evidence: str | None = None


# TODO error handling
@submissions_router.post('/api/submissions/edit/{submission_id}', tags=['Logged'])
async def edit_record(submission_id: str, data: EditSubmission, audit_id: int):
    edit_data = data.model_dump()

    to_edit = {}
    for key, value in edit_data.items():
        if value is not None:
            to_edit[key] = value


    query = {'_id': ObjectId(submission_id)}
    update = {'$set': to_edit}

    result = Mongo_Config.submissions.update_one(query, update)

    audit_log('edit_record', submission_id, audit_id, additional_info=to_edit)
    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/approve/{submission_id}', tags=['Logged'])
async def approve_record(submission_id: str, audit_id: int):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'APPROVED'}}

    result = Mongo_Config.submissions.update_one(query, update)

    audit_log('approve_record', submission_id, audit_id)
    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/deny/{submission_id}', tags=['Logged'])
async def deny_record(submission_id: str, audit_id: int):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'DENIED'}}

    result = Mongo_Config.submissions.update_one(query, update)

    audit_log('deny_record', submission_id, audit_id)
    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/get_pending', tags=['Unlogged'])
async def get_pending_records():
    query = {'status': 'PENDING'}

    documents = Mongo_Config.submissions.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return to_json


# TODO error handling
@submissions_router.get('/api/submissions/get_submissions/{user_id}', tags=['Unlogged'])
async def get_submissions(user_id: int):
    query = {'user_ids': user_id}

    documents = Mongo_Config.submissions.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return to_json

