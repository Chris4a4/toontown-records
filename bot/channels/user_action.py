from misc.auto_channel import AutoChannel
import discord
from misc.api_wrapper import request_namechange
from singletons.config import Config

from visuals.leaderboard import personal_leaderboard_paginator
from visuals.personal_bests import personal_bests_paginator, active_records_paginator
from visuals.submission_history import all_submissions_paginator


class UserActionChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.game = channel
        self.auto_channel = AutoChannel(bot, category, channel)
        self.welcome_string = f"Say hello to the <#{Config.WELCOME_CHANNEL_ID}> channel! In this channel, you may:\n- Set or change your display name\n- View your submission history, personal bests, and the records you're currently holding\n- Check your spot on the leaderboards"

    async def update(self):
        await self.auto_channel.update_all([(self.welcome_string, None, UserActionView(), [])])

class UserActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Change Display Name', style=discord.ButtonStyle.green, row=0)
    async def change_username_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = UsernameModal(title='Enter Display Name')
        await interaction.response.send_modal(modal)

    @discord.ui.button(label='View All Submissions', style=discord.ButtonStyle.blurple, row=1)
    async def submissions_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        avatar = interaction.user.avatar.url if interaction.user.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = all_submissions_paginator(interaction.user.id, avatar)

        if paginator:
            await paginator.respond(interaction, ephemeral=True)
        else:
            await interaction.response.send_message('User has no approved submissions!', ephemeral=True)

    @discord.ui.button(label='View Personal Bests', style=discord.ButtonStyle.blurple, row=1)
    async def pbs_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        avatar = interaction.user.avatar.url if interaction.user.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = personal_bests_paginator(interaction.user.id, avatar)

        if paginator:
            await paginator.respond(interaction, ephemeral=True)
        else:
            await interaction.response.send_message('User has no approved submissions!', ephemeral=True)

    @discord.ui.button(label='View Active Records', style=discord.ButtonStyle.blurple, row=1)
    async def records_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        avatar = interaction.user.avatar.url if interaction.user.avatar else Config.UNKNOWN_THUMBNAIL

        paginator = active_records_paginator(interaction.user.id, avatar)

        if paginator:
            await paginator.respond(interaction, ephemeral=True)
        else:
            await interaction.response.send_message('User has no approved submissions!', ephemeral=True)

    @discord.ui.button(label='View Leaderboard Positions', style=discord.ButtonStyle.grey, row=2)
    async def leaderboards_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        paginator = personal_leaderboard_paginator(interaction.user.id)

        if paginator:
            await paginator.respond(interaction, ephemeral=True)
        else:
            await interaction.response.send_message('User does not appear on any leaderboards!', ephemeral=True)


class UsernameModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label='Display Name', placeholder='Enter your display name here', max_length=20))

    async def callback(self, interaction: discord.Interaction):
        result = request_namechange(interaction.user.id, self.children[0].value, interaction.user.id)

        await interaction.response.send_message(result, ephemeral=True)