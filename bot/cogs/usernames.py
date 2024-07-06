from discord.ext import commands, tasks
import discord

from misc.api_wrapper import get_all_users
from misc.config import Config


class Usernames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.check_display_names.start()
    
    def cog_unload(self):
        self.check_display_names.cancel()
    
    # Assign role + change name to users in the discord
    @tasks.loop(minutes=1)
    async def check_display_names(self):
        print('Updating users...')
        name_to_id = get_all_users()
        id_to_name = {v: k for k, v in name_to_id.items()}

        for member in Config.GUILD.members:
            if member.id not in id_to_name:
                continue

            target_name = id_to_name[member.id]
            if member.display_name != target_name:
                try:
                    print(f'Changing name for {member.display_name} -> {target_name}')
                    await member.edit(nick=target_name)
                except discord.Forbidden:
                    print(f'Could not change name {member.display_name} -> {target_name}: No permission')

            if Config.AUTHORIZED_ROLE not in member.roles:
                await member.add_roles(Config.AUTHORIZED_ROLE)


def setup(bot):
    bot.add_cog(Usernames(bot))