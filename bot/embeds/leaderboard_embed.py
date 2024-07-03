from datetime import datetime, timezone

import discord


def leaderboard_embed(leaderboard_data, game, TOP_N=30):
    game_data = {
        'ttr': {
            'name': 'Toontown Rewritten',
            'icon': 'https://discord.do/wp-content/uploads/2023/08/Toontown-Rewritten.jpg',
            'color': discord.Colour.blurple()
        },
        'ttcc': {
            'name': 'Corporate Clash',
            'icon': 'https://cdn2.steamgriddb.com/icon_thumb/0cddee771b707457d155f0cdc477aef8.png',
            'color': discord.Colour.dark_red()
        },
        'overall': {
            'name': 'Overall',
            'icon': 'https://i.imgur.com/kEFU1YQ.png',
            'color': discord.Colour.yellow()
        }
    }[game]

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
    placement = 0
    leaderboard_string = ''
    for user in leaderboard[:TOP_N]:
        username = user['username']
        points = user['points']

        placement += 1
        if username:
            leaderboard_string += f'**{placement}.** {username} - {points} points\n'
        else:
            leaderboard_string += f'**{placement}.** ??? - {points} points\n'
    
    if not leaderboard_string:
        leaderboard_string = 'Coming soon...'

    embed.add_field(name=f'Top {TOP_N} users:', value=leaderboard_string, inline=False)

    return embed