from discord.ext import commands
from discord.utils import basic_autocomplete
from discord import Option, SlashCommandGroup, AutocompleteContext, Member
from singletons.channel_managers import ChannelManagers
from singletons.config import Config
from datetime import datetime
import math

from discord.ext import pages
from embeds.personal_bests_embed import personal_bests
from embeds.submission_history_embed import submission_history
from misc.api_wrapper import submit, edit_submission, approve_submission, deny_submission, get_all_users, get_all_info, get_approved_submissions, get_username
from misc.record_metadata import group_records, value_string


edit_fields = {
    'record_name': str,
    'user_ids': list[int],
    'value_score': int,
    'value_time': int,
    'evidence': str
}

async def users_autocomplete(ctx: AutocompleteContext):
    return get_all_users()


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Get all of a user's submissions, ordered by date
    @commands.user_command(name='View all submissions', description='Shows this users approved submissions')
    async def all_submissions(self, ctx, member: Member):
        MAX_PAGE = 30

        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL
        submissions = get_approved_submissions(member.id)
        username = get_username(member.id)
        
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
            submission_pages.append(submission_history(year, submissions, username, avatar))

        if submission_pages:
            paginator = pages.Paginator(pages=submission_pages)
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)


    # Get a user's best submissions, organized by record
    @commands.user_command(name='View personal bests', description='Shows this users personal bests')
    async def pbs(self, ctx, member: Member):
        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL

        pb_pages = []
        for mgr in ChannelManagers.record_channels:
            result = personal_bests(member.id, mgr.tags, avatar)

            if result:
                pb_pages.append(result)

        if pb_pages:
            paginator = pages.Paginator(pages=pb_pages)
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)

    # Get a user's active records, organized by record
    @commands.user_command(name='View active records', description='Shows this users active records')
    async def active_records(self, ctx, member: Member):
        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL

        pb_pages = []
        for mgr in ChannelManagers.record_channels:
            result = personal_bests(member.id, mgr.tags, avatar, records_only=True)

            if result:
                pb_pages.append(result)

        if pb_pages:
            paginator = pages.Paginator(pages=pb_pages)
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)

    # DEBUG COMMAND, commented out during normal use
    # Assumes 3 digit max score, H:MM:SS.mmm max time
    #@commands.slash_command(name='embed', description='Checks the max characters of all record embeds')
    async def embed_max_chars(self, ctx):
        MAX_USERNAME = 20

        big_submission = {
            'value_score': 100,
            'value_time': 4271111  # 1hr, 11m, 11s, 111ms
        }

        content = []
        for embed_name, records in group_records(get_all_info()).items():
            max_chars = len(embed_name)

            for record in records:
                max_chars += len(record['record_name'])

                max_chars += 2  # newlines
                max_chars += 3 * (3 + len(value_string(big_submission, record['tags'])))  # numbers, -, and score
                max_chars += 3 * (4 + 100)  # markdown + evidence link
                
                max_chars += 3 * record['max_players'] * MAX_USERNAME  # player names
                max_chars += 3 * (record['max_players'] - 1) * 2  # commas between player names

            content.append(f'{embed_name}: {max_chars}')

        await ctx.respond('\n'.join(content), ephemeral=True)

    # Submit
    @commands.slash_command(name='submit', description='Submits a record')
    async def submit_record(self, ctx,
        record: Option(str, 'Record name', required=True),
        evidence: Option(str, 'Link to record proof', required=True),
        time: Option(str, 'Record time in H:M:S form', required=False),
        score: Option(int, 'Record score', required=False),
        user1: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user2: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user3: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user4: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user5: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user6: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user7: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False),
        user8: Option(str, 'Record participants', autocomplete=basic_autocomplete(users_autocomplete), required=False)
    ):
        # Convert usernames to list
        usernames = [user1, user2, user3, user4, user5, user6, user7, user8]
        usernames = [u for u in usernames if u]

        data = {
            'record_name': record,
            'usernames': usernames,
            'value_score': score,
            'value_time': time,
            'evidence': evidence
        }
        result = submit(data, ctx.author.id)

        await ctx.respond(result, ephemeral=True)

    # Edit
    records = SlashCommandGroup('submissions', 'Manage submissions')
    @records.command(name='edit', description='Edit a submission')
    async def edit_submission(self, ctx,
        sid: Option(str, 'Submission ID to modify', required=True),
        field: Option(str, 'What to change', choices=edit_fields, required=True),
        value: Option(str, 'New value', required=True)
    ):
        value_type = edit_fields[field]

        try:
            if value == 'None':
                value_cast = None
            elif field == 'user_ids':
                values = value.strip('[]').split(',')
                value_cast = [int(v) for v in values]
            else:
                value_cast = value_type(value)

            result = edit_submission(sid, field, value_cast, ctx.author.id)
            
            await ctx.respond(result, ephemeral=True)

        except ValueError:
            await ctx.respond("Couldn't decipher that value", ephemeral=True)
    
    @records.command(name='approve', description='Approves a submission')
    async def approve_submission(self, ctx,
        sid: Option(str, 'Submission ID', required=True)
    ):
        result = approve_submission(sid, ctx.author.id)

        await ctx.respond(result, ephemeral=True)
    
    @records.command(name='deny', description='Denies a submission')
    async def deny_submission(self, ctx,
        sid: Option(str, 'Submission ID', required=True)
    ):
        result = deny_submission(sid, ctx.author.id)

        await ctx.respond(result, ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))