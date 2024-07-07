from discord.ext import commands, tasks

from singletons.channel_managers import ChannelManagers
from singletons.user_manager import UserManager


class ForceUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.force_update.start()
    
    def cog_unload(self):
        self.force_update.cancel()

    @tasks.loop(minutes=30)
    async def force_update(self):
        await ChannelManagers.force_update_all()
        await UserManager.force_update_all()


def setup(bot):
    bot.add_cog(ForceUpdate(bot))