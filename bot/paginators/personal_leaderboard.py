from embeds.leaderboard_embed import leaderboard_embed
from discord.ext import pages


def personal_leaderboard_paginator(user_id):
    leaderboard_pages = []
    for leaderboard in ['ttr', 'ttcc', 'overall']:
        result = leaderboard_embed(leaderboard, highlight_user_id=user_id)

        if result:
            leaderboard_pages.append(result)
    
    if leaderboard_pages:
        return pages.Paginator(pages=leaderboard_pages)
