import discord
from misc.api_wrapper import get_username, get_submissions, get_record_info
from misc.record_metadata import value_string

def all_submissions(user_id, avatar_url):
    username = get_username(user_id)
    submissions = get_submissions(user_id)

    embed = discord.Embed(
        title=f'Submissions with {username}',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)

    # Create strings for pending/approved submissions
    pending_strings = []
    approved_strings = []
    for s in submissions:
        record_name = s['record_name']
        record = get_record_info(record_name)

        if record:
            record_desc = f'{record_name} - [{value_string(s, record['tags'])}]({s['evidence']})'
            
            if s['status'] == 'PENDING':
                pending_strings.append(record_desc)
            elif s['status'] == 'APPROVED':
                approved_strings.append(record_desc)

    embed.add_field(name='Approved Submissions', value='\n'.join(approved_strings), inline=False)
    embed.add_field(name='Pending Submissions', value='\n'.join(pending_strings), inline=False)

    return embed