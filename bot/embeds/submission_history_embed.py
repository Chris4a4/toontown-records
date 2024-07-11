import discord
from misc.record_metadata import value_string
from misc.api_wrapper import get_record_info
from datetime import datetime
import math

def submission_history_embed(year_string, submissions, username, avatar_url):
    embed = discord.Embed(
        title=f'Submission history for {username}',
        description=f'Submissions in {year_string}',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)

    MAX_PAGE = 5

    # Group submissions by month
    submissions_by_month = {}
    for submission in submissions:
        month = datetime.fromtimestamp(submission['timestamp']).strftime('%B')

        if month in submissions_by_month:
            submissions_by_month[month].append(submission)
        else:
            submissions_by_month[month] = [submission]

    # Divide up any years with more than MAX_PAGE submissions
    submissions_divided = {}
    for month, submissions in submissions_by_month.items():
        num_pages = math.ceil(len(submissions) / MAX_PAGE)

        if num_pages == 1:
            submissions_divided[month] = submissions
            continue
        
        for page_num in range(0, num_pages):
            month_text = f'{month} (Part {page_num + 1})'
            index_from = page_num * MAX_PAGE
            index_to = (page_num + 1) * MAX_PAGE

            submissions_divided[month_text] = submissions[index_from:index_to]

    for month_string, month_submissions in submissions_divided.items():
        submission_strings = []
        for s in month_submissions:
            record = get_record_info(s['record_name'])

            if record:
                submission_strings.append(f'{record['record_name']} - [{value_string(s, record['tags'])}]({s['evidence']})')

        embed.add_field(name=month_string, value='\n'.join(submission_strings), inline=False)

    return embed