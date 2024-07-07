from discord.ext import commands
import re
import ast
from channels.channel_managers import ChannelManagers
from misc.config import Config
from embeds.submission_embed import submission_embed
import discord


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
        prioritize_dm = False
        if function == 'approve_namechange':
            user_id = params['discord_id']
            message = f'<@{user_id}> your namechange was approved! You are now {params['new_name']}.'
        
        elif function == 'deny_namechange':
            user_id = params['discord_id']
            message = f'<@{user_id}> your namechange was denied.'
            prioritize_dm = True

        elif function == 'approve_submission':
            user_id = params['submitter_id']
            message = f'<@{user_id}> your record was approved!'
            embed = submission_embed(params, mod=False)

        elif function == 'deny_submission':
            user_id = params['submitter_id']
            message = f'<@{user_id}> your submission for "{params['record_name']}" was denied.'
            prioritize_dm = True

        else:
            return
        
        # If the user isn't in the server, don't do anything at all
        user_ids = [member.id for member in Config.GUILD.members]
        if user_id not in user_ids:
            return

        # Prioritize sending a DM if the method type calls for it
        if prioritize_dm:
            try:
                user = self.bot.get_user(user_id)
                await user.send(message, embed=embed)
                return

            except discord.Forbidden:
                pass

        await Config.UPDATE_CHANNEL.send(message, embed=embed)


def setup(bot):
    bot.add_cog(Webhooks(bot))