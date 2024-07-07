from discord.ext import commands, tasks

from channels.channel_managers import ChannelManagers


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ChannelManagers.initialize(bot)

        self.force_update.start()
    
    def cog_unload(self):
        self.force_update.cancel()

    @tasks.loop(minutes=30)
    async def force_update(self):
        await ChannelManagers.force_update_all()


def setup(bot):
    bot.add_cog(Channels(bot))