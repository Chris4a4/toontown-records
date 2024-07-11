from fastapi import APIRouter
from collections import Counter
from api.records.records import lookup_all_record_info
from api.submissions.router import get_approved_submissions
from .leaderboards import update_record, get_top_N, find_placement

from copy import deepcopy

leaderboards_router = APIRouter()


@leaderboards_router.get('/api/leaderboards/update_database', tags=['Unlogged'])
async def update_database():
    for record in lookup_all_record_info():
        result = update_record(record['record_name'])

        if not result['success']:
            return {
                'success': False,
                'message': f'Error occured while updating record {record['record_name']}'
            }
    
    return {
        'success': True,
        'message': 'Updated leaderboards for all records'
    }


@leaderboards_router.get('/api/leaderboards/get_leaderboard/{game_id}', tags=['Unlogged'])
async def get_leaderboard(game_id: str):
    TOP1_BONUS_POINTS = 1
    TOP2_BONUS_POINTS = 1

    include_ttr = game_id == 'ttr' or game_id == 'overall'
    include_ttcc = game_id == 'ttcc' or game_id == 'overall'

    leaderboard = Counter()
    num_records = 0

    # Accumulate points for each record defined in records.yaml
    for record in lookup_all_record_info():
        name, points, tags = record['record_name'], record['points'], record['tags']

        including_game = ('ttr' in tags and include_ttr) or ('ttcc' in tags and include_ttcc)
        if not including_game:
            continue
        num_records += 1

        # First place bonus points
        best = get_top_N(name, 1)
        if not best:
            continue
        best = best[0]

        users = best['user_ids']
        for user in set(users):
            leaderboard.update({user: TOP1_BONUS_POINTS})
        
        # Top 2 bonus points
        top2 = get_top_N(name, 2)

        top2_users = []
        for submission in top2:
            top2_users.extend(submission['user_ids'])

        for user in set(top2_users):
            leaderboard.update({user: TOP2_BONUS_POINTS})

        # Top 3 get points
        top3 = get_top_N(name, 3)

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


# Gets the user's best placements
@leaderboards_router.get('/api/leaderboards/get_user_placements/{user_id}', tags=['Unlogged'])
async def get_user_placements(user_id: int):
    approved_submissions = (await get_approved_submissions(user_id))['data']

    result = []
    for record in lookup_all_record_info():
        best_placement = find_placement(record['record_name'], approved_submissions)

        if best_placement:
            record_copy = deepcopy(record)
            record_copy['placement'], record_copy['best'] = best_placement

            result.append(record_copy)

    return {
        'success': True,
        'message': 'Got users best placements',
        'data': result
    }
