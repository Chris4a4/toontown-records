import discord
from misc.record_metadata import value_string
from misc.api_wrapper import get_record_info

def submission_history(year_string, submissions, username, avatar_url):
    embed = discord.Embed(
        title=f'Submission history for {username}',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)

    submission_strings = []
    for s in submissions:
        record = get_record_info(s['record_name'])

        if record:
            submission_strings.append(f'<t:{s['timestamp']}:D> - {record['record_name']} - [{value_string(s, record['tags'])}]({s['evidence']})')

    embed.add_field(name=f'Submissions in {year_string}', value='\n'.join(submission_strings), inline=False)

    return embed