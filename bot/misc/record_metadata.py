from misc.time_helper import to_time
from functools import cache

import discord
import os


tags_to_details = {
    ('ttr', 'vp', 'nr', 'full'): ('VP Records', 'https://i.imgur.com/54nl5SN.png', 7489641, 'nr.png'),
    ('ttr', 'vp', 'nr', 'cog'): ('VP Cog Round Records', 'https://i.imgur.com/EPIyWNJ.jpeg', 7489641, 'nr.png'),
    ('ttr', 'vp', 'nr', 'pie'): ('VP Pie Round Records', 'https://i.imgur.com/A3l0ctU.png', 7489641, 'nr.png'),
    ('ttr', 'vp', 'rl', 'full'): ('Rewardless VP Records', 'https://i.imgur.com/54nl5SN.png', 7489641, 'rl.png'),
    ('ttr', 'vp', 'rl', 'cog'): ('Rewardless VP Cog Round Records', 'https://i.imgur.com/EPIyWNJ.jpeg', 7489641, 'rl.png'),
    ('ttr', 'vp', 'misc'): ('Miscellaneous VP Records', 'https://i.imgur.com/zeaOZxO.png', 7489641, 'misc-vp.png'),

    ('ttr', 'racing'): ('Racing Records', 'https://i.imgur.com/Lt7hLOZ.png', 16711680, 'racing.png'),
    ('ttr', 'golf'): ('Golfing Records', 'https://i.imgur.com/B56V0Lh.png', 5563476, 'golf.png'),
    ('ttr', ): ('Unknown Records', 'https://i.imgur.com/jgSzqns.png', 7489641, 'misc-vp.png')
}


def get_resource(file):
    image_path = os.path.join(os.path.dirname(__file__), '..', 'resources',  file)

    return discord.File(image_path, filename=file)


@cache
def get_metadata(record_tags):
    for check_tags, details in tags_to_details.items():
        if set(record_tags) == set(check_tags) | set(record_tags):
            return details


def group_records(records):
    result = {}

    for record in records:
        for check_tags, details in tags_to_details.items():
            record_tags = record['tags']

            if set(record_tags) == set(check_tags) | set(record_tags):
                category, thumbnail, color, banner = details

                if category in result:
                    result[category].append(record)
                else:
                    result[category] = [record]
                break
    
    return result


# Using a record's tags, correctly formats its score
def value_string(submission, tags=[]):
    score = submission['value_score']
    time = submission['value_time']

    time_string = to_time(time)

    # Format based on tags
    if 'golf' in tags:
        return f'{score} swings, {time_string}'
    
    if 'min_rewards' in tags:
        return f'{score} rewards, {time_string}'

    if tags:
        return time_string

    # Unknown record/no tags provided, use sensible default format
    if not time_string:
        return f'{score} score'

    if not score:
        return f'{time_string}'

    return f'{score} score, {time_string}'

    