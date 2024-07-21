from api.config.mongo_config import Mongo_Config
from api.config.config import Config
from fastapi import APIRouter
import requests

oauth_router = APIRouter()


@oauth_router.get('/api/oauth2/register/{code}', tags=['Unlogged'])
async def register(code: str):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'client_id': Config.OAUTH_CLIENT,
        'client_secret': Config.OAUTH_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': Config.OAUTH_URL
    }
    response = requests.post('https://discord.com/api/v10/oauth2/token', data=body, headers=header).json()

    if 'access_token' in response:
        token = response['access_token']

        Mongo_Config.oauth.insert_one({'token': token})

        return {
            'success': True,
            'message': 'Registered user token in database',
            'data': token
        }

    return {
        'success': False,
        'message': 'An error occured while calling OAuth',
        'data': None
    }


@oauth_router.get('/api/oauth2/get_info/{token}', tags=['Unlogged'])
async def get_info(token: str):
    if not Mongo_Config.oauth.find_one({'token': token}):
        return {
            'success': False,
            'message': 'Token is not registered in database',
            'data': None
        }
    
    header = {
         'Authorization': f'Bearer {token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=header).json()

    if 'id' not in response or 'avatar' not in response:
        return {
            'success': False,
            'message': 'Error occured while trying to access user data',
            'data': None
        }

    return {
        'success': True,
        'message': 'Got user data',
        'data': response
    }