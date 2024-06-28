from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder

from fastapi import APIRouter
from json import dumps, loads

users_router = APIRouter()


# Creates a user object if it doesn't already exist
def create_user(discord_id):
    if not Mongo_Config.users.find_one({"discord_id": discord_id}):
        # Object not found, create a new one
        new_object = {
            "discord_id": discord_id,
            "username": None,
            "desired_username": None
        }
        Mongo_Config.users.insert_one(new_object)


# Perform any checks before assigning a name
# 1. does someone already have/want this username?
def username_valid(discord_id, username):
    username_taken = {"username": username}
    desired_taken = {"desired_username": username}

    # If anyone has this username/desired username that ISN'T us, then it's invalid
    result = Mongo_Config.users.find({'$or': [username_taken, desired_taken]})
    for document in result:
        if not document['discord_id'] == discord_id:
            return False
    
    return True


# TODO error handling
@users_router.get('/api/users/get_username/{discord_id}')
async def get_username(discord_id: int):
    create_user(discord_id)

    user = Mongo_Config.users.find_one({"discord_id": discord_id})
    return user['username']


# TODO error handling
@users_router.get('/api/users/set_username/{discord_id}/{username}')
async def set_username(discord_id: int, username: str):
    create_user(discord_id)

    if not username_valid(discord_id, username):
        return {'status': 'username invalid'}

    query = {'discord_id': discord_id}
    update = {'$set': {'username': username, 'desired_username': username}}

    result = Mongo_Config.users.update_one(query, update)

    return {'status:': 'success'}


# TODO error handling
@users_router.get('/api/users/set_desired_username/{discord_id}/{username}')
async def set_desired_username(discord_id: int, username: str):
    create_user(discord_id)

    if not username_valid(discord_id, username):
        return {'status': 'username invalid'}

    query = {'discord_id': discord_id}
    update = {'$set': {'desired_username': username}}

    result = Mongo_Config.users.update_one(query, update)

    return {'status:': 'success'}


# TODO error handling
@users_router.get('/api/users/get_pending_users')
async def get_pending_users():
    query = {
        '$expr': {'$ne': ['$username', '$desired_username']}
    }

    documents = Mongo_Config.users.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return to_json


# TODO error handling
@users_router.get('/api/users/get_all_users')
async def get_all_users():
    query = {
        '$expr': {'$ne': ['$username', None]}
    }

    documents = Mongo_Config.users.find(query)
    
    result = {}
    for document in documents:
        result[document['discord_id']] = document['username']

    return result
