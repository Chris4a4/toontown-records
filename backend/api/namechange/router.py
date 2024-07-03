from fastapi import APIRouter
from bson.objectid import ObjectId
from json import dumps, loads
from time import time

from api.database.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder
from api.logging.logging import audit_log


namechange_router = APIRouter()


# Gets a user if it exists, otherwise creates it
def create_user(discord_id: int):
    # User already exists
    result = Mongo_Config.accounts.find_one({'discord_id': discord_id})
    if result:
        return result
    
    # User didn't exist
    new_user = {
        'discord_id': discord_id,
        'username': None
    }
    new_result = Mongo_Config.accounts.insert_one(new_user)

    return Mongo_Config.accounts.find_one({"_id": new_result.inserted_id})


# Marks a namechange request as approved
@namechange_router.get('/api/namechange/approve/{namechange_id}', tags=['Logged'])
async def approve_namechange(namechange_id: str, audit_id: int):
    namechange = Mongo_Config.namechanges.find_one({'_id': ObjectId(namechange_id)})
    new_name = namechange['new_username']
    discord_id = namechange['discord_id']

    # Update account document
    query = {'discord_id': discord_id}
    update = {'$set': {'username': new_name}}

    Mongo_Config.accounts.update_one(query, update)

    # Set namechange object to approved and log
    query = {'_id': ObjectId(namechange_id)}
    update = {'$set': {'status': 'APPROVED'}}

    Mongo_Config.namechanges.update_one(query, update)
    audit_log('approve_namechange', namechange_id, audit_id)
    return {
        'success': True,
        'message': 'Namechange request accepted'
    }


# Marks a namechange request as denied
@namechange_router.get('/api/namechange/deny/{namechange_id}', tags=['Logged'])
async def deny_namechange(namechange_id: str, audit_id: int):
    query = {'_id': ObjectId(namechange_id)}
    update = {'$set': {'status': 'DENIED'}}

    Mongo_Config.namechanges.update_one(query, update)
    audit_log('deny_namechange', namechange_id, audit_id)
    return {
        'success': True,
        'message': 'Namechange request denied'
    }


# Marks a namechange request as obsolete
@namechange_router.get('/api/namechange/obsolete/{namechange_id}', tags=['Logged'])
async def obsolete_namechange(namechange_id: str, audit_id: int):
    query = {'_id': ObjectId(namechange_id)}
    update = {'$set': {'status': 'OBSOLETE'}}

    Mongo_Config.namechanges.update_one(query, update)
    audit_log('obsolete_namechange', namechange_id, audit_id)
    return {
        'success': True,
        'message': 'Namechange request obsoleted'
    }


# Creates a namechange request for the user
@namechange_router.get('/api/namechange/request/{discord_id}/{username}', tags=['Logged'])
async def request_namechange(discord_id: int, username: str, audit_id: int):
    user = create_user(discord_id)

    # Verify that no one else has the name or has a pending namechange request for it
    taken_by_user = {'username': username}
    result_user = Mongo_Config.accounts.find(taken_by_user)

    taken_by_namechange = {
        'new_username': username,
        'status': 'PENDING'
    }
    result_namechange = Mongo_Config.accounts.find(taken_by_namechange)

    # If someone else has this username or is trying to change to it, return failure
    for document in list(result_user) + list(result_namechange):
        if document['discord_id'] != discord_id:
            return {
                'success': False,
                'message': f'Sorry, {username} is already in use'
            }

    # Obsolete any prior namechange requests
    query = {
        'discord_id': discord_id,
        'status': 'PENDING'
    }
    for document in Mongo_Config.namechanges.find(query):
        await obsolete_namechange(str(document['_id']), audit_id)

    # Put in the new namechange request
    namechange_request = {
        'discord_id': discord_id,
        'current_username': user['username'],
        'new_username': username,
        'submitter_id': audit_id,
        'timestamp': int(time()),
        'status': 'PENDING'
    }
    result = Mongo_Config.namechanges.insert_one(namechange_request)

    audit_log('request_namechange', str(result.inserted_id), audit_id)
    return {
        'success': True,
        'message': f'Request to change name to {username} submitted',
        'result_id': str(result.inserted_id)
    }


# Gets a list of all pending namechanges
@namechange_router.get('/api/namechange/get_pending', tags=['Unlogged'])
async def get_pending_namechanges():
    query = {'status': 'PENDING'}

    documents = Mongo_Config.namechanges.find(query)
    to_json = loads(dumps(list(documents), cls=MongoJSONEncoder))

    return {
        'success': True,
        'message': 'Got a list of all pending namechanges',
        'data': to_json
    }
