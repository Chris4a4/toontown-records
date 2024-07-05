import requests

from misc.config import Config

# TODO: change update times
# TODO: check for ", print statements, weird use of if
# TODO: add rest of records


########## RECORDS ##########
def get_record_info(record_name):
    return requests.get(f'{Config.BASE_URL}/records/get_info/{record_name}').json()['data']


def get_all_records():
    return requests.get(f'{Config.BASE_URL}/records/get_all_records').json()['data']


def get_leaderboard(game):
    return requests.get(f'{Config.BASE_URL}/records/get_leaderboard/{game}').json()['data']


########## SUBMISSIONS ##########
def submit(submission_data, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.post(f'{Config.BASE_URL}/submissions/submit', params=params, json=submission_data).json()['message']


def edit_submission(submission_id, field, value, audit_id):
    params = {
        'audit_id': audit_id
    }
    data = {field: value}
    return requests.post(f'{Config.BASE_URL}/submissions/edit/{submission_id}', params=params, json=data).json()['message']


def approve_submission(submission_id, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.get(f'{Config.BASE_URL}/submissions/approve/{submission_id}', params=params).json()['data']


def deny_submission(submission_id, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.get(f'{Config.BASE_URL}/submissions/deny/{submission_id}', params=params).json()['data']


def get_pending_submissions():
    return requests.get(f'{Config.BASE_URL}/submissions/get_pending').json()['data']

def get_submissions(user_id):
    return requests.get(f'{Config.BASE_URL}/submissions/get_submissions/{user_id}').json()['data']


########## ACCOUNTS ##########
def get_username(user_id):
    return requests.get(f'{Config.BASE_URL}/accounts/get_username/{user_id}').json()['data']


def get_all_users():
    return requests.get(f'{Config.BASE_URL}/accounts/get_all_users').json()['data']


########## NAMECHANGES ##########
def approve_namechange(namechange_id, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.get(f'{Config.BASE_URL}/namechange/approve/{namechange_id}', params=params).json()['message']


def deny_namechange(namechange_id, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.get(f'{Config.BASE_URL}/namechange/deny/{namechange_id}', params=params).json()['message']


def request_namechange(user_id, username, audit_id):
    params = {
        'audit_id': audit_id
    }
    return requests.get(f'{Config.BASE_URL}/namechange/request/{user_id}/{username}', params=params).json()['message']


def get_pending_namechanges():
    return requests.get(f'{Config.BASE_URL}/namechange/get_pending').json()['data']


########## LOGGING ##########
def get_logs():
    return requests.get(f'{Config.BASE_URL}/logging/get_logs').json()['data']
