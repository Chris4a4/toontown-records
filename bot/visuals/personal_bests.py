import discord
from misc.api_wrapper import get_username, get_user_placements
from misc.record_metadata import value_string, group_records
from singletons.config import Config
from discord.ext import pages


# Shows the user's best placement for each record
def personal_bests_paginator(user_id, avatar_url):
    pb_pages = []
    for channel_tags in Config.RECORD_CHANNELS:
        result = personal_bests_embed(user_id, channel_tags, avatar_url, 'personal bests')

        if result:
            pb_pages.append(result)

    if pb_pages:
        return pages.Paginator(pages=pb_pages)


# Only shows top3 placements
def active_records_paginator(user_id, avatar_url):
    pb_pages = []
    for channel_tags in Config.RECORD_CHANNELS:
        result = personal_bests_embed(user_id, channel_tags, avatar_url, 'active records')

        if result:
            pb_pages.append(result)

    if pb_pages:
        return pages.Paginator(pages=pb_pages)


def personal_bests_embed(user_id, tags, avatar_url, what_type):
    username = get_username(user_id)
    user_placements = get_user_placements(user_id)

    matching_placements = []
    for placement in user_placements:
        if set(placement['tags']) == set(tags) | set(placement['tags']):
            if what_type == 'active records' and placement['placement'] > 3:
                continue
            matching_placements.append(placement)

    # Return None if the user has no records with these tags
    if not matching_placements:
        return

    embed = discord.Embed(
        title=f"{username}'s {what_type}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)

    for group_name, records in group_records(matching_placements).items():
        descriptions = []
        for record in records:
            s = record['best']

            descriptions.append(f'**{record['placement']}.** {record['record_name']} - [{value_string(s, record['tags'])}]({s['evidence']})')

        embed.add_field(name=group_name, value='\n'.join(descriptions), inline=False)

    return embed