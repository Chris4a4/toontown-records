from discord.ext import pages
from singletons.config import Config
from embeds.personal_bests_embed import personal_bests_embed


# Shows the user's best placement for each record
def personal_bests_paginator(user_id, avatar_url):
    pb_pages = []
    for channel_tags in Config.RECORD_CHANNELS:
        result = personal_bests_embed(user_id, channel_tags, avatar_url)

        if result:
            pb_pages.append(result)

    if pb_pages:
        return pages.Paginator(pages=pb_pages)


# Only shows top3 placements
def active_records_paginator(user_id, avatar_url):
    pb_pages = []
    for channel_tags in Config.RECORD_CHANNELS:
        result = personal_bests_embed(user_id, channel_tags, avatar_url, records_only=True)

        if result:
            pb_pages.append(result)

    if pb_pages:
        return pages.Paginator(pages=pb_pages)
