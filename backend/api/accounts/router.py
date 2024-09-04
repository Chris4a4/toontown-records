from api.config.mongo_config import Mongo_Config

from fastapi import APIRouter

accounts_router = APIRouter()


@accounts_router.get('/api/accounts/get_username/{discord_id}', tags=['Unlogged'])
async def get_username(discord_id: int):
    user = Mongo_Config.accounts.find_one({'discord_id': discord_id})

    if user:
        username = user['username']

        if username:
            return {
                'success': True,
                'message': 'Found username',
                'data': username
            }

        return {
            'success': False,
            'message': 'Found user, but they did not have a username set',
            'data': '???'
        }

    return {
        'success': False,
        'message': 'User not found',
        'data': '???'
    }


@accounts_router.get('/api/accounts/get_all_users', tags=['Unlogged'])
async def get_all_users():
    query = {
        '$expr': {'$ne': ['$username', None]}
    }
    documents = Mongo_Config.accounts.find(query)
    
    result = {}
    for document in documents:
        result[document['username']] = document['discord_id']

    return {
        'success': True,
        'message': 'Generated username:user_id dictionary',
        'data': result
    }


@accounts_router.get('/api/accounts/update_pfp/{discord_id}', tags=['Unlogged'])
async def update_pfp(discord_id: int, pfp_link: str | None = None):
    if pfp_link:
        pfp_link = pfp_link.split('?')[0]
        pfp_link = pfp_link.replace('.png', '.webp')

        Mongo_Config.accounts.update_one({"discord_id": discord_id}, {"$set": {"pfp": pfp_link}})
    else:
        Mongo_Config.accounts.update_one({"discord_id": discord_id}, {"$set": {"pfp": None}})

    return {
        'success': True,
        'message': 'Updated profile picture',
    }


@accounts_router.get('/api/accounts/get_pfp/{discord_id}', tags=['Unlogged'])
async def get_pfp(discord_id: int):
    result = Mongo_Config.accounts.find_one({"discord_id": discord_id})

    if result:
        return {
            'success': True,
            'message': 'Retrieved profile picture for user',
            'data': result['pfp']
        }
    
    return {
        'success': False,
        'message': 'User not found',
        'data': None
    }