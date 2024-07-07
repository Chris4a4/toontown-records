from misc.api_wrapper import get_username
from singletons.config import Config
import discord

class UserManager():
    @classmethod
    async def force_update_all(cls):
        for member in Config.GUILD.members:
            await cls.update_one(member)
    
    @classmethod
    async def update_one(cls, member):
        username = get_username(member.id)

        # If they're not in the database, remove the authorized role if they have it
        if username == '???':
            if Config.AUTHORIZED_ROLE in member.roles:
                await member.remove_roles(Config.AUTHORIZED_ROLE)
            return

        # If they are in the database, check their name and give them the authorized role if they dont' have it
        if member.display_name != username:
            try:
                print(f'Changing name for {member.display_name} -> {username}')
                await member.edit(nick=username)
            except discord.Forbidden:
                print(f'Could not change name {member.display_name} -> {username}: No permission')

        if Config.AUTHORIZED_ROLE not in member.roles:
            await member.add_roles(Config.AUTHORIZED_ROLE)
    
    @classmethod
    async def update_from_id(cls, user_id):
        for member in Config.GUILD.members:
            if user_id == member.id:
                await cls.update_one(member)
                return
