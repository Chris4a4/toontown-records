from functools import cache

import discord
import os


TAGS_TO_DETAILS = {
    ('ttr', 'vp', 'nr', 'full'): ('VP Records', 'https://i.imgur.com/54nl5SN.png', 7489641, 'nr.png'),
    ('ttr', 'vp', 'nr', 'cog'): ('VP Cog Round Records', 'https://i.imgur.com/EPIyWNJ.jpeg', 7489641, 'nr.png'),
    ('ttr', 'vp', 'nr', 'pie'): ('VP Pie Round Records', 'https://i.imgur.com/A3l0ctU.png', 7489641, 'nr.png'),
    ('ttr', 'vp', 'rl', 'full'): ('Rewardless VP Records', 'https://i.imgur.com/54nl5SN.png', 7489641, 'rl.png'),
    ('ttr', 'vp', 'rl', 'cog'): ('Rewardless VP Cog Round Records', 'https://i.imgur.com/EPIyWNJ.jpeg', 7489641, 'rl.png'),
    ('ttr', 'vp', 'misc'): ('Miscellaneous VP Records', 'https://i.imgur.com/zeaOZxO.png', 7489641, 'misc-vp.png'),

    ('ttr', 'racing'): ('Racing Records', 'https://i.imgur.com/Lt7hLOZ.png', 16711680, 'racing.png'),
    ('ttr', 'golf'): ('Golfing Records', 'https://i.imgur.com/B56V0Lh.png', 5563476, 'golf.png')
}
UNKNOWN_DETAILS = 'Unknown Records', 'https://i.imgur.com/jgSzqns.png', 7489641, 'misc-vp.png'


def get_resource(file):
    image_path = os.path.join(os.path.dirname(__file__), '..', 'resources',  file)

    return discord.File(image_path, filename=file)


# Convert record_tags to a tuple so that @cache can hash it
def get_metadata(record_tags):
    return cached_get_metadata(tuple(record_tags))


@cache
def cached_get_metadata(record_tags):
    for check_tags, details in TAGS_TO_DETAILS.items():
        if set(record_tags) == set(check_tags) | set(record_tags):
            return details
    
    return UNKNOWN_DETAILS


# Groups records into a group:[records] dictionary
def group_records(records):
    result = {}

    for record in records:
        for check_tags, details in TAGS_TO_DETAILS.items():
            record_tags = record['tags']

            if set(record_tags) == set(check_tags) | set(record_tags):
                category, thumbnail, color, banner = details

                if category in result:
                    result[category].append(record)
                else:
                    result[category] = [record]
                break
    
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

    # Print the string depending on what kind of time it is
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
    else:
        score_string = score

    # Format based on tags
    if 'golf' in tags:
        return f'{score_string} swings, {time_string}'
    
    if 'min_rewards' in tags:
        return f'{score_string} rewards, {time_string}'

    if tags:
        return time_string

    # Unknown record/no tags provided, use sensible default format
    return f'{score_string} score, {time_string} time'
