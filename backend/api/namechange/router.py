import re
from fastapi import APIRouter
from bson.objectid import ObjectId
from json import dumps, loads
from time import time
from bson.errors import InvalidId

from api.config.mongo_config import Mongo_Config
from api.database.helper import MongoJSONEncoder
from api.logging.logging import audit_log
from api.logging.webhooks import send_webhook
from api.config.config import Config


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

    return Mongo_Config.accounts.find_one({'_id': new_result.inserted_id})


# Marks a namechange request as approved
@namechange_router.get('/api/namechange/approve/{namechange_id}', tags=['Logged'])
async def approve_namechange(namechange_id: str, audit_id: int):
    try:
        namechange_query = {
            '_id': ObjectId(namechange_id),
            'status': 'PENDING'
        }
    except InvalidId:
        return {
            'success': False,
            'message': 'Not a valid ID'
        }

    namechange = Mongo_Config.namechanges.find_one(namechange_query)
    if not namechange:
        return {
            'success': False,
            'message': 'Could not find a pending namechange with that ID'
        }

    old_name = namechange['current_username']
    new_name = namechange['new_username']
    discord_id = namechange['discord_id']

    # Update account document
    user_query = {'discord_id': discord_id}
    update = {'$set': {'username': new_name}}
    Mongo_Config.accounts.update_one(user_query, update)

    # Set namechange object to approved and log
    update = {'$set': {'status': 'APPROVED'}}
    Mongo_Config.namechanges.update_one(namechange_query, update)

    audit_log('approve_namechange', namechange_id, audit_id)
    send_webhook('approve_namechange', audit_id, discord_id, old_name, new_name)
    return {
        'success': True,
        'message': 'Namechange request accepted'
    }


# Marks a namechange request as denied
@namechange_router.get('/api/namechange/deny/{namechange_id}', tags=['Logged'])
async def deny_namechange(namechange_id: str, audit_id: int):
    try:
        namechange_query = {
            '_id': ObjectId(namechange_id),
            'status': 'PENDING'
        }
    except InvalidId:
        return {
            'success': False,
            'message': 'Not a valid ID'
        }

    namechange = Mongo_Config.namechanges.find_one(namechange_query)
    if not namechange:
        return {
            'success': False,
            'message': 'Could not find a pending namechange with that ID'
        }

    update = {'$set': {'status': 'DENIED'}}
    Mongo_Config.namechanges.update_one(namechange_query, update)

    audit_log('deny_namechange', namechange_id, audit_id)
    send_webhook('deny_namechange', audit_id, namechange['discord_id'], namechange['current_username'], namechange['new_username'])
    return {
        'success': True,
        'message': 'Namechange request denied'
    }


# Creates a namechange request for the user
@namechange_router.get('/api/namechange/request/{discord_id}/{username}', tags=['Logged'])
async def request_namechange(discord_id: int, username: str, audit_id: int):
    # Validate username
    if len(username) > Config.MAX_NAME_LEN:
        return {
            'success': False,
            'message': f'Names cannot be longer than {Config.MAX_NAME_LEN} characters'
        }
    
    if len(username) < Config.MIN_NAME_LEN:
        return {
            'success': False,
            'message': f'Names cannot be shorter than {Config.MIN_NAME_LEN} characters'
        }

    pattern = r'[^a-zA-Z0-9 ]'
    if re.search(pattern, username):
        return {
            'success': False,
            'message': 'Usernames can only contain letters, numbers, and spaces'
        }

    if '  ' in username:
        return {
            'success': False,
            'message': 'Usernames cannot have double spaces'
        }

    if username.startswith(' ') or username.endswith(' '):
        return {
            'success': False,
            'message': 'Usernames cannot start or end with spaces'
        }

    user = create_user(discord_id)

    # Verify that no one else has the name or has a pending namechange request for it
    taken_by_user = {'username': re.compile(username, re.IGNORECASE)}
    result_user = Mongo_Config.accounts.find(taken_by_user)

    taken_by_namechange = {
        'new_username': re.compile(username, re.IGNORECASE),
        'status': 'PENDING'
    }
    result_namechange = Mongo_Config.accounts.find(taken_by_namechange)

    # If someone else has this username or is trying to change to it, return failure
    for document in list(result_user) + list(result_namechange):
        if document['discord_id'] != discord_id:
            return {
                'success': False,
                'message': 'That name is already in use'
            }

    # Check if they already have a namechange request pending
    query = {
        'discord_id': discord_id,
        'status': 'PENDING'
    }
    if Mongo_Config.namechanges.find_one(query):
        return {
            'success': False,
            'message': 'You already have a pending namechange'
        }

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
    send_webhook('request_namechange', audit_id, discord_id, user['username'], username)
    return {
        'success': True,
        'message': 'Request to change name submitted',
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
