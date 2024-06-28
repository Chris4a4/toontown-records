from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder

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
@submissions_router.post('/api/submissions/submit')
async def submit(data: Submission):
    new_submission = data.model_dump()

    new_submission['date'] = int(time())
    new_submission['status'] = 'PENDING'

    result = Mongo_Config.records.insert_one(new_submission)

    return {'status:': 'success'}


class EditSubmission(BaseModel):
    record_name: str | None = None
    user_ids: List[int] | None = None
    value_score: int | None = None
    value_time: int | None = None
    evidence: str | None = None


# TODO error handling
@submissions_router.post('/api/submissions/edit/{submission_id}')
async def edit(submission_id: str, data: EditSubmission):
    to_edit = data.model_dump()

    query = {'_id': ObjectId(submission_id)}
    update = {'$set': to_edit}

    result = Mongo_Config.records.update_one(query, update)

    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/approve/{submission_id}')
async def approve(submission_id: str):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'APPROVED'}}

    result = Mongo_Config.records.update_one(query, update)

    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/deny/{submission_id}')
async def deny(submission_id: str):
    query = {'_id': ObjectId(submission_id)}
    update = {'$set': {'status': 'DENIED'}}

    result = Mongo_Config.records.update_one(query, update)

    return {'status:': 'success'}


# TODO error handling
@submissions_router.get('/api/submissions/get_all_pending')
async def get_all_pending():
    query = {'status': 'PENDING'}

    documents = Mongo_Config.records.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return to_json


# TODO error handling
@submissions_router.get('/api/submissions/get_submissions/{user_id}')
async def get_submissions(user_id: int):
    query = {'user_ids': user_id}

    documents = Mongo_Config.records.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return to_json

