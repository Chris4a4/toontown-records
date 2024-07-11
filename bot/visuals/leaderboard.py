from datetime import datetime, timezone

import discord

from misc.api_wrapper import get_leaderboard, get_username
from singletons.config import Config
from discord.ext import pages


def leaderboard_embed(game, highlight_user_id=None):
    game_data = {
        'ttr': {
            'name': 'Toontown Rewritten',
            'icon': Config.TTR_ICON,
            'color': Config.TTR_COLOR
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
    num_records = leaderboard_data['num_records']

    num_users = len(leaderboard)
    if num_users == 1:
        embed.description = f'This category has {num_records} available records and {num_users} scoring user'
    else:
        embed.description = f'This category has {num_records} available records and {num_users} scoring users'

    # Populate placement list
    found_highlighted_user = False
    leaderboard_string = ''
    for i, user in enumerate(leaderboard[:Config.LEADERBOARD_TOP_N]):
        user_id, points = user['user_id'], user['points']

        username = get_username(user_id)

        if highlight_user_id == user_id:
            leaderboard_string += f'--> __**{i + 1}.** {username} - {points} points__ <--\n'
            found_highlighted_user = True
        else:
            leaderboard_string += f'**{i + 1}.** {username} - {points} points\n'
    
    if not leaderboard_string:
        leaderboard_string = 'Coming soon...'

    embed.add_field(name=f'Top {Config.LEADERBOARD_TOP_N} users:', value=leaderboard_string, inline=False)

    if highlight_user_id and not found_highlighted_user:
        return None

    return embed


def personal_leaderboard_paginator(user_id):
    leaderboard_pages = []
    for leaderboard in Config.LEADERBOARDS:
        result = leaderboard_embed(leaderboard, highlight_user_id=user_id)

        if result:
            leaderboard_pages.append(result)
    
    if leaderboard_pages:
        return pages.Paginator(pages=leaderboard_pages)
