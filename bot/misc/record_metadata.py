import discord
import os
import yaml
from functools import cache
from PIL import Image, ImageDraw, ImageFont


# Recursive function to flatten out the nested dictionary format in record_metadata.yaml
def flatten_yaml(d):
    if not isinstance(d, dict):
        return [([], d)]

    result = []
    for k, v in d.items():
        new_tag = []
        if k:
            new_tag.append(k)

        for sub_tags, record_data in flatten_yaml(v):
            result.append((new_tag + sub_tags, record_data))

    return result


# Returns tuples of tags, details for all record groups, in order of importance
@cache
def tags_to_details():
    config_path = os.path.join(os.path.dirname(__file__), 'data', 'record_metadata.yaml')

    with open(config_path, 'r') as file:
        data = yaml.safe_load(file)

    return flatten_yaml(data)


# Draws a banner and saves it to a file
def get_banner(banner_text, text_color):
    text_color = tuple(text_color)
    filename = banner_text + '.png'

    # Check if it already exists
    image_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'banners',  filename)
    if os.path.exists(image_path):
        return discord.File(image_path, filename=filename)

    # Base image
    base_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'base',  'banner_base.png')
    base = Image.open(base_path)
    draw = ImageDraw.Draw(base)

    # Font
    font_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'font',  'Minnie.ttf')
    font_size = 36
    text_font = ImageFont.truetype(font_path, font_size)
    outline_width = 2
    outline_color = int(text_color[0] / 3), int(text_color[1] / 3), int(text_color[2] / 3)

    # Draw over base image
    if banner_text.endswith(' Records'):
        banner_text = banner_text[:-8]
    banner_text = '• ' + banner_text + ' •'
    draw.text((3, 0), banner_text, font=text_font, fill=text_color, stroke_width=outline_width, stroke_fill=outline_color)

    # Save
    base.save(image_path) 

    return discord.File(image_path, filename=filename)


# Gets the metadata associated with a set of record tags, found in record_metadata.yaml
def get_metadata(record_tags):
    for check_tags, details in tags_to_details():
        if set(record_tags) == set(check_tags) | set(record_tags):
            return details


# Groups records into a group:[records] dictionary
def group_records(records):
    result = {}

    for record in records:
        for check_tags, details in tags_to_details():
            record_tags = record['tags']

            if set(record_tags) == set(check_tags) | set(record_tags):
                category, thumbnail, color, banner_color = details

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
        score_plural = 's'
    else:
        score_string = score
        score_plural = '' if score == 1 else 's'

    # Format based on tags
    if 'golf' in tags:
        return f'{score_string} swing{score_plural}, {time_string}'
    
    if 'min_rewards' in tags:
        return f'{score_string} reward{score_plural}, {time_string}'

    if tags:
        return time_string

    # Unknown record/no tags provided, use sensible default format
    return f'{score_string} score, {time_string} time'
