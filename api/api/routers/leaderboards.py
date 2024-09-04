from fastapi import APIRouter

from api.backend.wrapper import get_leaderboard, get_all_users, get_pfp

leaderboards_router = APIRouter()


@leaderboards_router.get('/api/leaderboards/top3')
async def top3():
    leaderboard = get_leaderboard('overall')['leaderboard'][:3]

    name_to_id = get_all_users()
    id_to_name = {v: k for k, v in name_to_id.items()}

    for user in leaderboard:
        user['username'] = id_to_name[user['user_id']]
        user['pfp'] = get_pfp(user['user_id'])

    return leaderboard