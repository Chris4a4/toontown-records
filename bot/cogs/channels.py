from discord.ext import commands, tasks

from channels.leaderboard_channel import LeaderboardChannelManager
from channels.log_channel import LogChannelManager
from channels.namechange_channel import NamechangeChannelManager
from channels.records_channel import RecordChannelManager
from channels.submissions_channel import SubmissionsChannelManager


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channels = [
            LeaderboardChannelManager(bot, 'leaderboards', 'ttr'),
            LeaderboardChannelManager(bot, 'leaderboards', 'ttcc'),
            LeaderboardChannelManager(bot, 'leaderboards', 'overall'),
            LogChannelManager(bot, 'mods', 'logs'),
            RecordChannelManager(bot, 'ttr', 'vp'),
            RecordChannelManager(bot, 'ttr', 'activities'),
            SubmissionsChannelManager(bot, 'mods', 'pending-records'),
            NamechangeChannelManager(bot, 'mods', 'pending-namechanges')
        ]

        self.update_channels.start()
    
    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=1)
    async def update_channels(self):
        for channel_manager in self.channels:
            await channel_manager.update()


def setup(bot):
    bot.add_cog(Channels(bot))