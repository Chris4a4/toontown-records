from discord.ext import commands, tasks

from channels.leaderboard_channel import LeaderboardChannelManager
from channels.log_channel import LogChannelManager
from channels.namechange_channel import NamechangeChannelManager
from channels.records_channel import RecordChannelManager
from channels.submissions_channel import SubmissionsChannelManager


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.mod_channels = [
            LogChannelManager(bot, 'mods', 'logs'),
            SubmissionsChannelManager(bot, 'mods', 'pending-records'),
            NamechangeChannelManager(bot, 'mods', 'pending-namechanges')
        ]
        self.user_channels = [
            LeaderboardChannelManager(bot, 'leaderboards', 'ttr'),

            RecordChannelManager(bot, 'ttr', 'vp'),
            RecordChannelManager(bot, 'ttr', 'cfo'),
            RecordChannelManager(bot, 'ttr', 'cj'),
            RecordChannelManager(bot, 'ttr', 'ceo'),
            RecordChannelManager(bot, 'ttr', 'activities'),
        ]

        self.frequent_update.start()
        self.infrequent_update.start()
    
    def cog_unload(self):
        self.frequent_update.cancel()
        self.infrequent_update.cancel()

    @tasks.loop(minutes=1)
    async def frequent_update(self):
        for channel_manager in self.mod_channels:
            await channel_manager.update()
    
    @tasks.loop(minutes=15)
    async def infrequent_update(self):
        for channel_manager in self.user_channels:
            await channel_manager.update()


def setup(bot):
    bot.add_cog(Channels(bot))