from discord.ext import commands, tasks
import discord

from misc.api_wrapper import get_all_users
from misc.config import Config


class Usernames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role = discord.utils.get(Config.GUILD.roles, name=Config.AUTHORIZED_ROLE)

        self.check_display_names.start()
    
    def cog_unload(self):
        self.check_display_names.cancel()
    
    # Assign role + change name to users in the discord
    @tasks.loop(minutes=1)
    async def check_display_names(self):
        name_dict = get_all_users()

        for member in Config.GUILD.members:
            if member.id not in name_dict:
                continue

            if member.display_name != name_dict[member.id]:
                try:
                    await member.edit(nick=name_dict[member.id])
                except discord.Forbidden:
                    pass
            else:
                if self.role not in member.roles:
                    await member.add_roles(self.role)


def setup(bot):
    bot.add_cog(Usernames(bot))