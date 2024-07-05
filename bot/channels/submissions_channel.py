import requests
from embeds.submission_embed import submission_embed
from channels.auto_channel import AutoChannel
import discord

class SubmissionsChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        submissions = requests.get(f'http://backend:8000/api/submissions/get_pending').json()['data']

        result = []
        for submission in submissions:
            embed = submission_embed(submission)
            result.append(('', embed, SubmmissionView(submission['record_name'], str(submission['_id'])), []))
        
        await self.auto_channel.apply(result)


class SubmmissionView(discord.ui.View):
    def __init__(self, record_name, submission_id):
        super().__init__()
        self.record_name = record_name
        self.submission_id = submission_id

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
    async def approve_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = {
            'audit_id': interaction.user.id
        }
        result = requests.get(f'http://backend:8000/api/submissions/approve/{self.submission_id}', params=params).json()

        await self.message.delete()
        await interaction.response.send_message(result['message'], ephemeral=True)

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def deny_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = {
            'audit_id': interaction.user.id
        }
        result = requests.get(f'http://backend:8000/api/submissions/deny/{self.submission_id}', params=params).json()

        await self.message.delete()
        await interaction.response.send_message(result['message'], ephemeral=True)