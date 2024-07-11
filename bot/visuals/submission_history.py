import discord
from misc.record_metadata import value_string
from misc.api_wrapper import get_record_info
from datetime import datetime
import math
from discord.ext import pages
from misc.api_wrapper import get_approved_submissions, get_username


MAX_PAGE = 30
MAX_SUB_PAGE = 5


def all_submissions_paginator(user_id, avatar):
    submissions = get_approved_submissions(user_id)
    username = get_username(user_id)
    
    # Group submissions by year
    submissions_by_year = {}
    for submission in submissions:
        year = datetime.fromtimestamp(submission['timestamp']).year

        if year in submissions_by_year:
            submissions_by_year[year].append(submission)
        else:
            submissions_by_year[year] = [submission]

    # Divide up any years with more than MAX_PAGE submissions
    submissions_divided = {}
    for year, submissions in submissions_by_year.items():
        num_pages = math.ceil(len(submissions) / MAX_PAGE)

        if num_pages == 1:
            submissions_divided[str(year)] = submissions
            continue
        
        for page_num in range(0, num_pages):
            year_text = f'{year} (Part {page_num + 1})'
            index_from = page_num * MAX_PAGE
            index_to = (page_num + 1) * MAX_PAGE

            submissions_divided[year_text] = submissions[index_from:index_to]

    # Create pages
    submission_pages = []
    for year, submissions in submissions_divided.items():
        submission_pages.append(submission_history_embed(year, submissions, username, avatar))
    
    if submission_pages:
        return pages.Paginator(pages=submission_pages)


def submission_history_embed(year_string, submissions, username, avatar_url):
    embed = discord.Embed(
        title=f'Submission history for {username}',
        description=f'Submissions in {year_string}',
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=avatar_url)

    # Group submissions by month
    submissions_by_month = {}
    for submission in submissions:
        month = datetime.fromtimestamp(submission['timestamp']).strftime('%B')

        if month in submissions_by_month:
            submissions_by_month[month].append(submission)
        else:
            submissions_by_month[month] = [submission]

    # Divide up any years with more than MAX_SUB_PAGE submissions
    submissions_divided = {}
    for month, submissions in submissions_by_month.items():
        num_pages = math.ceil(len(submissions) / MAX_SUB_PAGE)

        if num_pages == 1:
            submissions_divided[month] = submissions
            continue
        
        for page_num in range(0, num_pages):
            month_text = f'{month} (Part {page_num + 1})'
            index_from = page_num * MAX_SUB_PAGE
            index_to = (page_num + 1) * MAX_SUB_PAGE

            submissions_divided[month_text] = submissions[index_from:index_to]

    for month_string, month_submissions in submissions_divided.items():
        submission_strings = []
        for s in month_submissions:
            record = get_record_info(s['record_name'])

            if record:
                submission_strings.append(f'{record['record_name']} - [{value_string(s, record['tags'])}]({s['evidence']})')

        embed.add_field(name=month_string, value='\n'.join(submission_strings), inline=False)

    return embed