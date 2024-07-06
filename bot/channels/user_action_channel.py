from channels.auto_channel import AutoChannel
import discord
from misc.api_wrapper import request_namechange

class UserActionChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.game = channel
        self.auto_channel = AutoChannel(bot, category, channel)

    async def update(self):
        await self.auto_channel.apply([('yo', None, UserActionView(), [])])

class UserActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Change Display Name', style=discord.ButtonStyle.blurple)
    async def change_username_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = UsernameModal(title='Enter Display Name')
        await interaction.response.send_modal(modal)

class UsernameModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label='Display Name', placeholder='Enter your display name here', max_length=20))

    async def callback(self, interaction: discord.Interaction):
        result = request_namechange(interaction.user.id, self.children[0].value, interaction.user.id)

        

        await interaction.response.send_message(result, ephemeral=True)