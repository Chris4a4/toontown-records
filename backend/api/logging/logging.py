from bson.objectid import ObjectId
from api.config.mongo_config import Mongo_Config

from time import time


LOGGED_FUNCTIONS = [
    'submit',
    'edit_submission',
    'approve_submission',
    'deny_submission',
    'request_namechange',
    'approve_namechange',
    'deny_namechange'
]

FUNCTION_TO_TYPE = {
    'submit': 'submission',
    'request_namechange': 'namechange'
}


# Logs an action. If it's a submission/namechange request, make a new entry in the logging database. Otherwise, append to the existing entry
def audit_log(function, document_id, audit_id, additional_info=None):
    # If it's a submit/namechange request, make a new document in database
    if function in FUNCTION_TO_TYPE:
        new_log = {
            'type': FUNCTION_TO_TYPE[function],
            'document': ObjectId(document_id),
            'modifications': []
        }
        Mongo_Config.audit_log.insert_one(new_log)
    
    # Append the operation info to the log object in the database
    action_info = {
        'timestamp': int(time()),
        'audit_id': audit_id,
        'operation': function,
        'additional_info': additional_info
    }
    filter = {'document': ObjectId(document_id)}
    update = {'$push': {'modifications': action_info}}
    Mongo_Config.audit_log.update_one(filter, update)
