from datetime import datetime, timezone

import discord

from misc.api_wrapper import get_leaderboard, get_username
from singletons.config import Config
from discord.ext import pages

GAME_DATA = {
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
}


def personal_leaderboard_paginator(user_id):
    leaderboard_pages = []
    for leaderboard in Config.LEADERBOARDS:
        result = personal_leaderboard_embed(leaderboard, user_id)

        if result:
            leaderboard_pages.append(result)
    
    if leaderboard_pages:
        return pages.Paginator(pages=leaderboard_pages)


def personal_leaderboard_embed(game, highlight_user_id):
    leaderboard_data = get_leaderboard(game)

    # Find user's place and prune records around it
    leaderboard = leaderboard_data['leaderboard']
    for i, user in enumerate(leaderboard):
        user_id = user['user_id']

        if user_id == highlight_user_id:
            index = i
            break
    else:
        return None
    
    bottom_index = index - 2
    top_index = index + 3
    if bottom_index < 0:  # Move window up as far as possible
        top_index -= bottom_index
        bottom_index = 0
    elif top_index > len(leaderboard):  # Move window down as far as possible
        diff = top_index - len(leaderboard)
        top_index -= diff
        bottom_index = max(0, bottom_index - diff)

    pruned_leaderboard = list(enumerate(leaderboard))[bottom_index:top_index]

    # Generate the leaderboard with minor differences
    data = GAME_DATA[game]

    embed = discord.Embed(
        title=f'{data['name']} Leaderboard',
        timestamp=datetime.now(timezone.utc),
        color=data['color']
    )
    embed.set_thumbnail(url=data['icon'])

    num_records = leaderboard_data['num_records']

    num_users = len(leaderboard)
    if num_users == 1:
        embed.description = f'This category has {num_records} available records and {num_users} scoring user'
    else:
        embed.description = f'This category has {num_records} available records and {num_users} scoring users'

    # Populate placement list
    leaderboard_string = ''
    for i, user in pruned_leaderboard:
        user_id, points = user['user_id'], user['points']

        username = get_username(user_id)

        if user_id == highlight_user_id:
            leaderboard_string += f'--> __**{i + 1}.** {username} - {points} points__ <--\n'
        else:
            leaderboard_string += f'**{i + 1}.** {username} - {points} points\n'

    embed.add_field(name=f'Nearby users:', value=leaderboard_string, inline=False)

    return embed


def leaderboard_embed(game):
    leaderboard_data = get_leaderboard(game)
    data = GAME_DATA[game]

    embed = discord.Embed(
        title=f'{data['name']} Leaderboard',
        timestamp=datetime.now(timezone.utc),
        color=data['color']
    )
    embed.set_thumbnail(url=data['icon'])

    leaderboard = leaderboard_data['leaderboard']
    num_records = leaderboard_data['num_records']

    num_users = len(leaderboard)
    if num_users == 1:
        embed.description = f'This category has {num_records} available records and {num_users} scoring user'
    else:
        embed.description = f'This category has {num_records} available records and {num_users} scoring users'

    # Populate placement list
    leaderboard_string = ''
    for i, user in enumerate(leaderboard[:Config.LEADERBOARD_TOP_N]):
        user_id, points = user['user_id'], user['points']

        username = get_username(user_id)

        leaderboard_string += f'**{i + 1}.** {username} - {points} points\n'
    
    if not leaderboard_string:
        leaderboard_string = 'Coming soon...'

    embed.add_field(name=f'Top {Config.LEADERBOARD_TOP_N} users:', value=leaderboard_string, inline=False)

    return embed
