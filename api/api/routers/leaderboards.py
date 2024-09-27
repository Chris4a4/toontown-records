from fastapi import APIRouter
import re

from api.backend.wrapper import get_leaderboard, get_all_users, get_pfp, get_recent, get_record_info, get_all_records

leaderboards_router = APIRouter()


@leaderboards_router.get('/api/leaderboards/records')
async def records():
    records = []
    raw_data = get_all_records()

    name_to_id = get_all_users()
    id_to_name = {v: k for k, v in name_to_id.items()}

    for record in raw_data:
        new_data = {}
        new_data['record_name'] = record['record_name']
        new_data['tags'] = record['tags']
        if record['top3']:
            best_submission = record['top3'][0]
            new_data['value'] = value_string(best_submission, record['tags'])
            new_data['submitters'] = ', '.join([id_to_name[user_id] for user_id in best_submission['user_ids']])
        else:
            new_data['value'] = None
            new_data['submitters'] = 'No Submissions'
        
        records.append(new_data)

    return records


@leaderboards_router.get('/api/leaderboards/top3')
async def top3():
    leaderboard = get_leaderboard('overall')['leaderboard'][:3]

    name_to_id = get_all_users()
    id_to_name = {v: k for k, v in name_to_id.items()}

    for user in leaderboard:
        user['username'] = id_to_name[user['user_id']]
        user['pfp'] = get_pfp(user['user_id'])

    return leaderboard


@leaderboards_router.get('/api/leaderboards/recent')
async def recent():
    result = []
    name_to_id = get_all_users()
    id_to_name = {v: k for k, v in name_to_id.items()}

    for record in get_recent():
        item = {}

        item['record_name'] = record['record_name']
        item['usernames'] = ', '.join([id_to_name[user_id] for user_id in record['user_ids']])

        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:embed\/|v\/|watch\?v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, record['evidence'])
        
        if match:
            video_id = match.group(1)
            item['thumbnail_url'] = f'https://i.ytimg.com/vi_webp/{video_id}/hqdefault.webp'
            item['embed_url'] = f'https://www.youtube.com/embed/{video_id}'
        else:
            item['thumbnail_url'] = None
            item['embed_url'] = None
        
        record_tags = get_record_info(record['record_name'])
        score_string = value_string(record, record_tags)
        item['score_string'] = score_string

        result.append(item)

    return result


# Converts ms to a time string
def to_time(ms):
    # Compute hours, minutes, seconds, and milleseconds
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    if ms == 0:
        ms_part = ''
    else:
        ms_part = f'.{ms:03d}'

    # Format the string depending on what kind of time it is
    if not h == 0:
        return f'{h}:{m:02d}:{s:02d}{ms_part}'
    elif not m == 0:
        return f'{m}:{s:02d}{ms_part}'

    return f'{s}{ms_part}'


# Using a record's tags, correctly formats its score
def value_string(submission, tags=[]):
    score = submission['value_score']
    time = submission['value_time']

    # Check for null
    if time is None:
        time_string = '???'
    else:
        time_string = to_time(time)

    if score is None:
        score_string = '???'
        score_plural = 's'
    else:
        score_string = score
        score_plural = '' if score == 1 else 's'

    # Format based on tags
    if 'golf' in tags:
        return f'{score_string} swing{score_plural}, {time_string}'
    
    if 'min_rewards' in tags:
        return f'{score_string} reward{score_plural}, {time_string}'

    if tags:
        return time_string

    # Unknown record/no tags provided, use sensible default format
    return f'{score_string} score, {time_string} time'
