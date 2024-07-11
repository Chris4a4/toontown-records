import discord

from misc.record_metadata import get_metadata, value_string
from misc.api_wrapper import get_record_info, get_username


def submission_embed(submission, fields):
    record_name = submission['record_name']
    record_info = get_record_info(record_name)

    # Actual record
    if record_info:
        tags = record_info['tags']
        category, thumbnail, color, banner = get_metadata(tags)

        value_desc = value_string(submission, tags=tags)
    # Unknown record
    else:
        category, thumbnail, color, banner = get_metadata([])

        value_desc = value_string(submission)

    # Names
    names = []
    for user_id in submission['user_ids']:
        username = get_username(user_id)

        names.append(username)

    names_string = ', '.join(names)

    embed = discord.Embed(
        title=record_name,
        description=f'{names_string} - [{value_desc}]({submission['evidence']})\nSubmitted at <t:{submission['timestamp']}:f>',
        thumbnail=thumbnail,
        color=color
    )

    if fields == 'pending' or fields == 'logs':
        # Raw data
        raw_data = []
        for key, value in submission.items():
            raw_data.append(f'{key}: {value}')
        embed.add_field(name='Raw Data:', value=f'```{'\n'.join(raw_data)}```', inline=False)

    if fields == 'logs':
        # Approve/deny/edit
        embed.add_field(name='Approve:', value=f'```/submissions approve sid:{str(submission['_id'])}```', inline=False)
        embed.add_field(name='Deny:', value=f'```/submissions deny sid:{str(submission['_id'])}```', inline=False)
        embed.add_field(name='Edit:', value=f'```/submissions edit sid:{str(submission['_id'])} field: value:```', inline=False)

    return embed