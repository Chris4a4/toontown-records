import discord

from misc.record_metadata import get_metadata, value_string
from misc.api_wrapper import get_username


def records_embed(records):
    category, thumbnail, color, banner_color = get_metadata(records[0]['tags'])

    embed = discord.Embed(
        title=f'**{category}**',
        thumbnail=thumbnail,
        color=color
    )

    # Body
    for record in records:
        points = record['points']
        if points == 1:
            title = f'__{record['record_name']}__'
        else:
            title = f'__{record['record_name']}__ - ``{points} points``'

        top_3 = record['top3']
        if not top_3:
            embed.add_field(name=title, value='N/A', inline=False)
        else:
            descriptions = []
            for i, submission in enumerate(top_3):
                # Names
                names = []
                for user_id in submission['user_ids']:
                    username = get_username(user_id)

                    names.append(username)

                names_string = ', '.join(names)

                # Value
                value_desc = value_string(submission, tags=record['tags'])
                descriptions.append(f'**{i + 1}.** {names_string} - [{value_desc}]({submission['evidence']})')

            # Join top 3 and make a field
            desc = '\n'.join(descriptions)
            desc += '\n'
            embed.add_field(name=title, value=desc, inline=False)

    return embed