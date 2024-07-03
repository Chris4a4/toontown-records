from embeds.namechange_embed import namechange_embed
from channels.auto_channel import AutoChannel
import discord
import requests

class NamechangeChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        pending_namechanges = requests.get(f'http://backend:8000/api/namechange/get_pending').json()['data']

        result = []
        for namechange in pending_namechanges:
            embed = namechange_embed(namechange)

            result.append(('', embed, NamechangeView(namechange), []))

        await self.auto_channel.apply(result)


class NamechangeView(discord.ui.View):
    def __init__(self, namechange):
        super().__init__()
        self.namechange_id = namechange['_id']

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
    async def approve_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = {
            'audit_id': {interaction.user.id}
        }
        result = requests.get(f'http://backend:8000/api/namechange/approve/{self.namechange_id}', params=params).json()

        await self.message.delete()
        await interaction.response.send_message(result['message'], ephemeral=True)

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def deny_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        params = {
            'audit_id': {interaction.user.id}
        }
        result = requests.get(f'http://backend:8000/api/namechange/deny/{self.namechange_id}', params=params).json()

        await self.message.delete()
        await interaction.response.send_message(result['message'], ephemeral=True)