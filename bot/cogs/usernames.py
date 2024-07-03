from discord.ext import commands, tasks
import discord
import requests


class Usernames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.check_display_names.start()
    
    def cog_unload(self):
        self.check_display_names.cancel()
    
    @tasks.loop(minutes=1)
    async def check_display_names(self):
        name_dict = requests.get(f'http://backend:8000/api/accounts/get_all_users').json()
        name_dict = {int(k): v for k, v in name_dict.items()}

        guild = self.bot.guilds[0]
        for member in guild.members:
            if member.id not in name_dict:
                requests.get(f'http://backend:8000/api/accounts/create/{member.id}')
                print(f'created a user for {member.name}')
                name_dict = requests.get(f'http://backend:8000/api/accounts/get_all_users').json()
                name_dict = {int(k): v for k, v in name_dict.items()}

            if member.display_name != name_dict[member.id]:
                try:
                    await member.edit(nick=name_dict[member.id])
                    print(f'Changed nickname for {member.name}')
                except discord.Forbidden:
                    print(f'Could not change nickname for {member.name}: Missing permissions')


def setup(bot):
    bot.add_cog(Usernames(bot))