from discord.ext import commands
from discord.commands import slash_command
from discord import Option, SlashCommandGroup
import requests

from misc.time_helper import to_ms


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

    records = SlashCommandGroup('submissions', 'Manage submissions')
    @records.command(name='edit', description='Edit a submission')
    async def edit_submission(self, ctx,
        id: Option(str, 'Submission ID to modify', required=True),
        field: Option(str, 'What to change', choices=edit_fields, required=True),
        value: Option(str, 'New value', required=True)
    ):
        value_type = edit_fields[field]

        try:
            if field == 'user_ids':
                values = value.strip('[]').split(',')
                value_cast = [int(v) for v in values]
            else:
                value_cast = value_type(value)

            params = {
                'audit_id': ctx.author.id
            }
            data = {field: value_cast}
            requests.post(f'http://backend:8000/api/submissions/edit/{id}', params=params, json=data)
            
            await ctx.respond(f'Performed Edit:\n```_id: {id}\n{field}: {value}```', ephemeral=True)
        except ValueError:
            await ctx.respond(f'Invalid Value:\n```{field}: {value}```', ephemeral=True)


    @commands.slash_command(name='username', description='Requests a namechange')
    async def request_namechange(self, ctx,
        username: Option(str, 'New username', required=True)
    ):
        params = {
            'audit_id': {ctx.author.id}
        }
        result = requests.get(f'http://backend:8000/api/namechange/request/{ctx.author.id}/{username}', params=params).json()

        await ctx.respond(result['message'], ephemeral=True)
    
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
        # Get record data
        record_data = requests.get(f'http://backend:8000/api/records/get_info/{record}').json()['data']
        if not record_data:
            await ctx.respond(f"I couldn't find a record named ``{record}``", ephemeral=True)

        # Get all username:user_id pairs
        id_to_username = requests.get(f'http://backend:8000/api/accounts/get_all_users').json()
        username_to_id = {value: key for key, value in id_to_username.items()}

        # Convert usernames to IDs
        users = [user1, user2, user3, user4, user5, user6, user7, user8]
        users = [u for u in users if u]
        
        max_players = record_data['max_players']
        if len(users) > max_players:
            await ctx.respond(f'This record has a max players of ``{max_players}``', ephemeral=True)
            return

        user_ids = []
        for user in users:
            if user in username_to_id:
                user_ids.append(username_to_id[user])
            else:
                await ctx.respond(f"I couldn't find a user with the username ``{user}``", ephemeral=True)
                return
        
        # Check values/time
        if record_data['score_required'] and not score:
            await ctx.respond(f'This record requires a score', ephemeral=True)
            return
        
        if record_data['time_required'] and not time:
            await ctx.respond(f'This record requires a time', ephemeral=True)
            return
        
        if time and not record_data['time_required']:
            await ctx.respond(f"You can't submit a time for this record", ephemeral=True)
            return
        
        if score and not record_data['score_required']:
            await ctx.respond(f"You can't submit a score for this record", ephemeral=True)
            return

        if time:
            try:
                time = to_ms(time)
            except ValueError:
                await ctx.respond(f"I don't understand the time ``{time}``\n```Valid Time Formats:\nH:M:S ex. 4:30:24\nM:S ex. 3:23\nS ex. 4.5```", ephemeral=True)
                return
        
        params = {
            'audit_id': ctx.author.id
        }
        data = {
            'record_name': record,
            'submitter_id': ctx.author.id,
            'user_ids': user_ids,
            'value_score': score,
            'value_time': time,
            'evidence': evidence
        }
        requests.post(f'http://backend:8000/api/submissions/submit', params=params, json=data)

        raw_data = []
        for key, value in data.items():
            raw_data.append(f'{key}: {value}')
        await ctx.respond(f'Record Submitted:\n```{'\n'.join(raw_data)}```', ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))