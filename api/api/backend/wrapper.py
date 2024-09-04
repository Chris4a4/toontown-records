import requests

def get_all_users():
    return requests.get(f'http://backend:8000/api/accounts/get_all_users').json()['data']

def get_leaderboard(game):
    return requests.get(f'http://backend:8000/api/leaderboards/get_leaderboard/{game}').json()['data']

def get_pfp(user_id):
    return requests.get(f'http://backend:8000/api/accounts/get_pfp/{user_id}').json()['data']