from embeds.namechange_embed import namechange_embed
from channels.auto_channel import AutoChannel
import discord
from misc.api_wrapper import get_pending_namechanges, approve_namechange, deny_namechange

class NamechangeChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        pending_namechanges = get_pending_namechanges()

        result = []
        for namechange in pending_namechanges:
            embed = namechange_embed(namechange)

            result.append(('', embed, NamechangeView(namechange), []))

        await self.auto_channel.apply(result)


class NamechangeView(discord.ui.View):
    def __init__(self, namechange):
        super().__init__(timeout=None)
        self.namechange_id = namechange['_id']

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
    async def approve_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        result = approve_namechange(self.namechange_id, interaction.user.id)

        await self.message.delete()
        await interaction.response.send_message(result, ephemeral=True)

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def deny_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        result = deny_namechange(self.namechange_id, interaction.user.id)

        await self.message.delete()
        await interaction.response.send_message(result, ephemeral=True)