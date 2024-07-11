from discord.ext import commands
from discord.utils import basic_autocomplete
from discord import Option, SlashCommandGroup, AutocompleteContext, Member
from singletons.config import Config

from paginators.personal_leaderboard import personal_leaderboard_paginator
from paginators.personal_bests import personal_bests_paginator, active_records_paginator
from paginators.all_submissions import all_submissions_paginator

from misc.api_wrapper import submit, edit_submission, approve_submission, deny_submission, get_all_users, get_all_info
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
        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = all_submissions_paginator(member.id, avatar)

        if paginator:
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)


    # Get a user's best submissions, organized by record
    @commands.user_command(name='View personal bests', description='Shows this users personal bests')
    async def pbs(self, ctx, member: Member):
        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = active_records_paginator(member.id, avatar)

        if paginator:
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)

    # Get a user's active records, organized by record
    @commands.user_command(name='View active records', description='Shows this users active records')
    async def active_records(self, ctx, member: Member):
        avatar = member.avatar.url if member.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = personal_bests_paginator(member.id, avatar)

        if paginator:
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User has no approved submissions!', ephemeral=True)


    # Get a user's leaderboard positions
    @commands.user_command(name='View leaderboard positions', description='Shows this users leaderboard positions')
    async def leaderboard_positions(self, ctx, member: Member):
        paginator = personal_leaderboard_paginator(member.id)

        if paginator:
            await paginator.respond(ctx.interaction, ephemeral=True)
        else:
            await ctx.respond('User does not appear on any leaderboards!', ephemeral=True)


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