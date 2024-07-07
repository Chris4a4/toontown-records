from discord.ext import commands
from discord.utils import basic_autocomplete
from discord import Option, SlashCommandGroup, Interaction, User, AutocompleteContext
from singletons.config import Config

from embeds.all_submissions_embed import all_submissions
from misc.api_wrapper import submit, edit_submission, approve_submission, deny_submission, get_all_users


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

    # Get a user's submissions
    @commands.user_command(name='Get submissions', description='Gets all submissions by a user')
    async def get_submissions(self, interaction: Interaction, user: User):
        if user.avatar:
            embed = all_submissions(user.id, user.avatar.url)
        else:
            embed = all_submissions(user.id, Config.UNKNOWN_THUMBNAIL)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    
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