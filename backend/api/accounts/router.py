from pydantic import BaseModel
from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder

from fastapi import APIRouter
from json import dumps, loads

accounts_router = APIRouter()


@accounts_router.get('/api/accounts/create/{discord_id}', tags=['Unlogged'])
async def create_user(discord_id: int):
    if not Mongo_Config.accounts.find_one({"discord_id": discord_id}):
        # Object not found, create a new one
        new_object = {
            "discord_id": discord_id,
            "username": f'temp-{discord_id}',
            "desired_username": f'temp-{discord_id}'
        }
        Mongo_Config.accounts.insert_one(new_object)


# TODO error handling
@accounts_router.get('/api/accounts/get_username/{discord_id}', tags=['Unlogged'])
async def get_username(discord_id: int):
    user = Mongo_Config.accounts.find_one({"discord_id": discord_id})
    return user['username']


# TODO error handling
@accounts_router.get('/api/accounts/get_all_users', tags=['Unlogged'])
async def get_all_users():
    query = {
        '$expr': {'$ne': ['$username', None]}
    }

    documents = Mongo_Config.accounts.find(query)
    
    result = {}
    for document in documents:
        result[document['discord_id']] = document['username']

    return result
