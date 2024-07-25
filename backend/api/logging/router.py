from bson.objectid import ObjectId
from api.config.mongo_config import Mongo_Config
from api.database.helper import docs_to_json

from fastapi import APIRouter

logging_router = APIRouter()


@logging_router.get('/api/logging/get_logs', tags=['Unlogged'])
async def get_logs():
    # Get all log objects from the database
    logs = Mongo_Config.audit_log.find()
    json_logs = docs_to_json(logs)

    # Replace the "document" attribute with the actual content instead of just a link to it
    for log in json_logs:
        if log['type'] == 'namechange':
            collection = Mongo_Config.namechanges
        else:
            collection = Mongo_Config.submissions

        query = {'_id': ObjectId(log['document'])}
        document = collection.find_one(query)
        document['_id'] = log['document']

        log['document'] = document

    return {
        'success': True,
        'message': 'Got a list of all log data',
        'data': json_logs
    }