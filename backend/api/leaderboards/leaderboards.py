from api.records.records import counts_for_this, lookup_record_info, get_sorting
from api.config.mongo_config import Mongo_Config

from api.database.helper import doc_to_json


# User_submissions is a list of all approved submissions by a user
# Returns the user's best placement for this record + submission associated with it, if they have one
def find_placement(record_name, user_submissions):
    leaderboard_ids = lookup_leaderboard(record_name)
    id_to_submission = {submission['_id']:submission for submission in user_submissions}

    for i, placement_id in enumerate(leaderboard_ids):
        if str(placement_id) in id_to_submission:
            return i + 1, id_to_submission[str(placement_id)]


# Finds the ordered list of IDs associated with a record
def lookup_leaderboard(record_name):
    leaderboard_query = {'record_name': record_name}
    leaderboard = Mongo_Config.leaderboard.find_one(leaderboard_query)
    if not leaderboard:
        raise ValueError(f'Could not find leaderboard info: {record_name}')

    return leaderboard['leaderboard']


# Returns an ordered list of the n best submissions for a particular record, if they exist
def get_top_N(record_name, top_n):
    leaderboard_ids = lookup_leaderboard(record_name)[:top_n]

    # Get all the submissions in the leaderboard in a dictionary and use the original list to sort them
    submission_query = {'_id': {'$in': leaderboard_ids}}
    submissions = Mongo_Config.submissions.find(submission_query)
    submissions_dict = {doc['_id']: doc for doc in submissions}

    sorted_submissions = [submissions_dict[doc_id] for doc_id in leaderboard_ids]
    to_json = doc_to_json(sorted_submissions)

    return to_json


def update_record(record_name: str):
    record_data = lookup_record_info(record_name)
    if not record_data:
        return {
            'success': False,
            'message': 'Record not found'
        }

    # Sort/aggregate submissions to form the leaderboard
    records_to_check = counts_for_this(record_name)
    sorting = get_sorting(record_data['tags'])
    pipeline = [
        {
            '$match': {
                'record_name': {'$in': records_to_check},
                'status': 'APPROVED'
            }
        },
        {
            '$sort': sorting
        },
        {
            '$group': {
                '_id': '$user_ids',
                'document': { '$first': '$$ROOT' }
            }
        },
        {
            '$replaceRoot': {
                'newRoot': '$document'
            }
        },
        {
            '$sort': sorting
        }
    ]
    documents = Mongo_Config.submissions.aggregate(pipeline)
    record_ids = [doc['_id'] for doc in documents]

    # Update 
    query = {'record_name': record_name}
    update_data = {'$set': {'leaderboard': record_ids}}

    Mongo_Config.leaderboard.update_one(query, update_data, upsert=True)

    return {
        'success': True,
        'message': 'Updated leaderboard'
    }
