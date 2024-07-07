from discord.ext import commands
import re
import ast
from channels.channel_managers import ChannelManagers
from misc.config import Config
from embeds.submission_embed import submission_embed


class Webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore non webhooks
        if message.channel.id != Config.WEBHOOK_CHANNEL_ID or not message.webhook_id:
            await self.bot.process_commands(message)
            return

        # Convert to a dictionary using regex magic
        params = {}
        for key, value in re.compile(r'(\w+)=([^\|]+)').findall(message.content):
            try:
                if value.startswith('[') and value.endswith(']'):  # Special case for user_id list
                    params[key] = ast.literal_eval(value)
                elif value == 'None':
                    params[key] = None
                else:
                    params[key] = int(value)
            except (ValueError, SyntaxError):
                params[key] = value

        await self.process_webhook(params)

    # Given a valid webhook, update necessary channels and create a message
    async def process_webhook(self, params):
        await self.send_update_message(params)
        await ChannelManagers.update_from_function(params['function'])
    
    # Sends a message in the update channel informing the submitter that something has happened
    async def send_update_message(self, params):
        function = params['function']

        embed = None
        if function == 'approve_namechange':
            message = f'<@{params['discord_id']}> your namechange was approved! You are now {params['new_name']}.'
        
        elif function == 'deny_namechange':
            message = f'<@{params['discord_id']}> your namechange was denied.'

        elif function == 'approve_submission':
            message = f'<@{params['submitter_id']}> your record was approved!'
            embed = submission_embed(params, mod=False)

        elif function == 'deny_submission':
            message = f'<@{params['submitter_id']}> your submission for "{params['record_name']}" was denied.'

        else:
            return

        await Config.UPDATE_CHANNEL.send(message, embed=embed)


def setup(bot):
    bot.add_cog(Webhooks(bot))