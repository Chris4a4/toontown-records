import discord
from misc.api_wrapper import get_username, get_user_placements
from misc.record_metadata import value_string, group_records

def personal_bests(user_id, tags, avatar_url, records_only=False):
    username = get_username(user_id)
    user_placements = get_user_placements(user_id)

    matching_placements = []
    for placement in user_placements:
        if set(placement['tags']) == set(tags) | set(placement['tags']):
            if records_only and placement['placement'] > 3:
                continue
            matching_placements.append(placement)

    # Return None if the user has no records with these tags
    if not matching_placements:
        return

    embed = discord.Embed(
        title=f'Personal bests for {username}',
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