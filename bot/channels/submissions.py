from visuals.submission import submission_embed
from misc.auto_channel import AutoChannel
import discord
from misc.api_wrapper import get_pending_submissions, approve_submission, deny_submission


class SubmissionsChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        content = []
        for submission in get_pending_submissions():
            embed = submission_embed(submission, 'pending')
            content.append(('', embed, SubmmissionView(submission['record_name'], str(submission['_id'])), []))
        
        await self.auto_channel.update_all(content)


class SubmmissionView(discord.ui.View):
    def __init__(self, record_name, submission_id):
        super().__init__(timeout=None)
        self.record_name = record_name
        self.submission_id = submission_id

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.green)
    async def approve_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        result = approve_submission(self.submission_id, interaction.user.id)

        await self.message.delete()
        await interaction.response.send_message(result, ephemeral=True)

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def deny_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        result = deny_submission(self.submission_id, interaction.user.id)

        await self.message.delete()
        await interaction.response.send_message(result, ephemeral=True)
    
    @discord.ui.button(label='Edit', style=discord.ButtonStyle.blurple)
    async def edit_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f'```/submissions edit sid:{self.submission_id} field: value:```', ephemeral=True)