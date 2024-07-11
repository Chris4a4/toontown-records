import math
from datetime import datetime
from misc.api_wrapper import get_approved_submissions, get_username
from embeds.submission_history_embed import submission_history_embed
from discord.ext import pages

MAX_PAGE = 30


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