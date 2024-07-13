from discord.ext import commands, tasks

from misc.api_wrapper import update_database
from singletons.channel_managers import ChannelManagers
from singletons.user_manager import UserManager

from asyncio import TaskGroup
import discord


class ForceUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.force_update.start()
    
    def cog_unload(self):
        self.force_update.cancel()

    @tasks.loop(hours=4)
    async def force_update(self):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('Updating channels...'))
        
        update_database()

        async with TaskGroup() as tg:
            tg.create_task(ChannelManagers.force_update_all())
            tg.create_task(UserManager.force_update_all())

        await self.bot.change_presence(status=discord.Status.idle, activity=None)


def setup(bot):
    bot.add_cog(ForceUpdate(bot))