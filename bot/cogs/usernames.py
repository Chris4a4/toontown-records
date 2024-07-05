from discord.ext import commands, tasks
import discord
import requests


class Usernames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.check_display_names.start()
    
    def cog_unload(self):
        self.check_display_names.cancel()
    
    # Assign role to users in the 
    @tasks.loop(minutes=1)
    async def check_display_names(self):
        guild = self.bot.guilds[0]

        name_dict = requests.get(f'http://backend:8000/api/accounts/get_all_users').json()['data']

        role_name = 'basic rights'
        role = discord.utils.get(guild.roles, name=role_name)

        for member in guild.members:
            if member.id not in name_dict:
                continue

            if member.display_name != name_dict[member.id]:
                try:
                    await member.edit(nick=name_dict[member.id])
                    print(f'Changed nickname for {member.name}')
                except discord.Forbidden:
                    print(f'Could not change nickname for {member.name}: Missing permissions')
            else:
                if role and role not in member.roles:

                    await member.add_roles(role)
                    print(f'Assigned {role.name} to {member.name}')


def setup(bot):
    bot.add_cog(Usernames(bot))