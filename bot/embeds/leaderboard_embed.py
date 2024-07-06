from datetime import datetime, timezone

import discord

from misc.api_wrapper import get_leaderboard, get_username
from misc.config import Config

def leaderboard_embed(game):
    game_data = {
        'ttr': {
            'name': 'Toontown Rewritten',
            'icon': Config.TTR_ICON,
            'color': Config.TTR_ICON
        },
        'ttcc': {
            'name': 'Corporate Clash',
            'icon': Config.TTCC_ICON,
            'color': Config.TTCC_COLOR
        },
        'overall': {
            'name': 'Overall',
            'icon': Config.OVERALL_ICON,
            'color': Config.OVERALL_COLOR
        }
    }[game]

    leaderboard_data = get_leaderboard(game)

    embed = discord.Embed(
        title=f'{game_data['name']} Leaderboard',
        timestamp=datetime.now(timezone.utc),
        color=game_data['color']
    )
    embed.set_thumbnail(url=game_data['icon'])

    leaderboard = leaderboard_data['leaderboard']
    max_points = leaderboard_data['max_points']

    num_users = len(leaderboard)
    if num_users == 1:
        embed.description = f'This category has {max_points} available points and {num_users} unique user'
    else:
        embed.description = f'This category has {max_points} available points and {num_users} unique users'

    # Populate placement list
    leaderboard_string = ''
    for i, user in enumerate(leaderboard[:Config.LEADERBOARD_TOP_N]):
        user_id, points = user['user_id'], user['points']

        username = get_username(user_id)

        leaderboard_string += f'**{i + 1}.** {username} - {points} points\n'
    
    if leaderboard_string:
        leaderboard_string = 'Coming soon...'

    embed.add_field(name=f'Top {Config.LEADERBOARD_TOP_N} users:', value=leaderboard_string, inline=False)

    return embed