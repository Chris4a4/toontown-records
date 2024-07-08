from collections import Counter
from .records import lookup_all_record_info, lookup_record_info, get_top_N
from fastapi import APIRouter
from copy import deepcopy

records_router = APIRouter()


# Gets the record information for a given record
@records_router.get('/api/records/get_info/{record_name}', tags=['Unlogged'])
async def get_record_info(record_name: str):
    record_data = lookup_record_info(record_name)

    if record_data:
        return {
            'success': True,
            'message': 'Got record information',
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
    records = deepcopy(lookup_all_record_info())
    for record in records:
        record['top3'] = get_top_N(record, 3)

    return {
        'success': True,
        'message': 'Got all record data',
        'data': records
    }


# Gets the user's best placements
@records_router.get('/api/records/get_user_placements/{user_id}', tags=['Unlogged'])
async def get_user_placements(user_id: int):
    result = []
    for record in lookup_all_record_info():
        all_placements = get_top_N(record, None)

        for i, placement in enumerate(all_placements):
            if user_id in placement['user_ids']:
                record_copy = deepcopy(record)

                record_copy['best'] = placement
                record_copy['placement'] = i + 1
                result.append(record_copy)
                break

    return {
        'success': True,
        'message': 'Got users best placements',
        'data': result
    }


@records_router.get('/api/records/get_leaderboard/{game_id}', tags=['Unlogged'])
async def get_leaderboard(game_id):
    FIRST_PLACE_BONUS_POINTS = 1

    include_ttr = game_id == 'ttr' or game_id == 'overall'
    include_ttcc = game_id == 'ttcc' or game_id == 'overall'

    leaderboard = Counter()
    num_records = 0

    # Accumulate points for each record defined in records.yaml
    for record in lookup_all_record_info():
        points, tags = record['points'], record['tags']

        including_game = ('ttr' in tags and include_ttr) or ('ttcc' in tags and include_ttcc)
        if not including_game:
            continue
        num_records += 1

        # First place bonus points
        best = get_top_N(record, 1)
        if not best:
            continue
        best = best[0]

        users = best['user_ids']
        for user in set(users):
            leaderboard.update({user: FIRST_PLACE_BONUS_POINTS})
        
        # Top 3 get points
        top3 = get_top_N(record, 3)

        top3_users = []
        for submission in top3:
            top3_users.extend(submission['user_ids'])

        for user in set(top3_users):
            leaderboard.update({user: points})
    
    # Sort and tally results
    result = {
        'num_records': num_records,
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
