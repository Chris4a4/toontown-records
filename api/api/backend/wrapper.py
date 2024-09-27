import requests

def get_all_users():
    return requests.get(f'http://backend:8000/api/accounts/get_all_users').json()['data']

def get_leaderboard(game):
    return requests.get(f'http://backend:8000/api/leaderboards/get_leaderboard/{game}').json()['data']

def get_pfp(user_id):
    return requests.get(f'http://backend:8000/api/accounts/get_pfp/{user_id}').json()['data']

def get_recent():
    return requests.get(f'http://backend:8000/api/submissions/get_recent').json()['data']

def get_record_info(record_name):
    return requests.get(f'http://backend:8000/api/records/get_info/{record_name}').json()['data']

def get_all_records():
    return requests.get(f'http://backend:8000/api/records/get_all_records').json()['data']