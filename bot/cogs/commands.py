from discord.ext import commands
from discord.commands import slash_command
from discord import Option, SlashCommandGroup
import requests


edit_fields = {
    'record_name': str,
    'user_ids': list[int],
    'value_score': int,
    'value_time': int,
    'evidence': str
}

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Namechange
    @commands.slash_command(name='username', description='Requests a namechange')
    async def request_namechange(self, ctx,
        username: Option(str, 'New username', required=True)
    ):
        params = {
            'audit_id': {ctx.author.id}
        }
        result = requests.get(f'http://backend:8000/api/namechange/request/{ctx.author.id}/{username}', params=params).json()

        await ctx.respond(result['message'], ephemeral=True)
    
    # Submit
    @commands.slash_command(name='submit', description='Submits a record')
    async def submit_record(self, ctx,
        record: Option(str, 'Record name', required=True),
        evidence: Option(str, 'Link to record proof', required=True),
        time: Option(str, 'Record time in H:M:S form', required=False),
        score: Option(int, 'Record score', required=False),
        user1: Option(str, 'Record participants', required=False),
        user2: Option(str, 'Record participants', required=False),
        user3: Option(str, 'Record participants', required=False),
        user4: Option(str, 'Record participants', required=False),
        user5: Option(str, 'Record participants', required=False),
        user6: Option(str, 'Record participants', required=False),
        user7: Option(str, 'Record participants', required=False),
        user8: Option(str, 'Record participants', required=False)
    ):
        # Convert usernames to list
        usernames = [user1, user2, user3, user4, user5, user6, user7, user8]
        usernames = [u for u in usernames if u]
        
        params = {
            'audit_id': ctx.author.id
        }
        data = {
            'record_name': record,
            'usernames': usernames,
            'value_score': score,
            'value_time': time,
            'evidence': evidence
        }
        result = requests.post(f'http://backend:8000/api/submissions/submit', params=params, json=data).json()

        await ctx.respond(result['message'], ephemeral=True)

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

            params = {
                'audit_id': ctx.author.id
            }
            data = {field: value_cast}
            result = requests.post(f'http://backend:8000/api/submissions/edit/{sid}', params=params, json=data).json()
            
            await ctx.respond(result['message'], ephemeral=True)

        except ValueError:
            await ctx.respond("Couldn't decipher that value", ephemeral=True)
    
    @records.command(name='approve', description='Approves a submission')
    async def approve_submission(self, ctx,
        sid: Option(str, 'Submission ID', required=True)
    ):
        params = {
            'audit_id': {ctx.author.id}
        }
        result = requests.get(f'http://backend:8000/api/submissions/approve/{sid}', params=params).json()

        await ctx.respond(result['message'], ephemeral=True)
    
    @records.command(name='deny', description='Denies a submission')
    async def deny_submission(self, ctx,
        sid: Option(str, 'Submission ID', required=True)
    ):
        params = {
            'audit_id': {ctx.author.id}
        }
        result = requests.get(f'http://backend:8000/api/submissions/deny/{sid}', params=params).json()

        await ctx.respond(result['message'], ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))