from collections import Counter
from .records import lookup_all_record_info, lookup_record_info, get_top_N
from fastapi import APIRouter

records_router = APIRouter()


# Gets the record information for a given record
@records_router.get('/api/records/get_info/{record_name}', tags=['Unlogged'])
async def get_record_info(record_name: str):
    record_data = lookup_record_info(record_name)

    if record_data:
        return {
            'success': True,
            'message': f'Got record information',
            'data': record_data
        }

    return {
        'success': False,
        'message': 'Could not find given record',
        'data': None
    }


# Gets the record information for every record
@records_router.get('/api/records/get_all_info', tags=['Unlogged'])
async def get_all_record_info():
    all_data = lookup_all_record_info()

    return {
        'success': True,
        'message': 'Got data for all records',
        'data': all_data
    }


# Gets the record information and top3 information for every record
@records_router.get('/api/records/get_all_records', tags=['Unlogged'])
async def get_all_records():
    records = lookup_all_record_info()
    for record in records:
        record['top3'] = get_top_N(record, 3)

    return {
        'success': True,
        'message': 'Got all record data',
        'data': records
    }


@records_router.get('/api/records/get_leaderboard/{game_id}', tags=['Unlogged'])
async def get_leaderboard(game_id):
    include_ttr = game_id == 'ttr' or game_id == 'overall'
    include_ttcc = game_id == 'ttcc' or game_id == 'overall'

    leaderboard = Counter()
    max_points = 0

    # Accumulate points for each record defined in records.yaml
    for record in lookup_all_record_info():
        points, tags = record['points'], record['tags']

        including_game = ('ttr' in tags and include_ttr) or ('ttcc' in tags and include_ttcc)
        if not including_game:
            continue
        max_points += points

        # Get the best placement if it exists
        best = get_top_N(record, 1)
        if not best:
            continue
        best = best[0]

        # Loop through users and add points for them
        users = best['user_ids']
        for user in set(users):
            leaderboard.update({user: points})
    
    # Sort and tally results
    result = {
        'max_points': max_points,
        'leaderboard': []
    }
    for user_id, user_points in leaderboard.most_common():
        result['leaderboard'].append({
            'user_id': user_id,
            'points': user_points
        })

    return {
        'success': True,
        'message': 'Populated leaderboard',
        'data': result
    }
