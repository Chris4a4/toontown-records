from misc.api_wrapper import get_username
from singletons.config import Config
import discord
from asyncio import TaskGroup
from misc.api_wrapper import get_leaderboard

class UserManager():
    @classmethod
    async def force_update_all(cls):
        async with TaskGroup() as tg:
            tg.create_task(cls.update_all_leaderboard_roles())
            for member in Config.GUILD.members:
                tg.create_task(cls.update_name(member))
    
    @classmethod
    async def update_name(cls, member):
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
                await cls.update_name(member)
                return

    @classmethod
    async def update_all_leaderboard_roles(cls):
        leaderboard_data = get_leaderboard('overall')['leaderboard']

        top_1_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(1, len(leaderboard_data)))]
        top_3_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(3, len(leaderboard_data)))]
        top_10_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(10, len(leaderboard_data)))]

        async with TaskGroup() as tg:
            for member in Config.GUILD.members:
                tg.create_task(cls.update_leaderboard_roles(member, top_1_ids=top_1_ids,  top_3_ids=top_3_ids,  top_10_ids=top_10_ids))

    @classmethod
    async def update_leaderboard_roles(cls, member, top_1_ids=None, top_3_ids=None, top_10_ids=None):
        if top_1_ids == None:
            leaderboard_data = get_leaderboard('overall')['leaderboard']

            top_1_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(1, len(leaderboard_data)))]
            top_3_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(3, len(leaderboard_data)))]
            top_10_ids = [leaderboard_data[i]['user_id'] for i in range(0, min(10, len(leaderboard_data)))]

        # Top 1
        if member.id in top_1_ids and Config.TOP_1_ROLE not in member.roles:
            await member.add_roles(Config.TOP_1_ROLE)
        
        elif Config.TOP_1_ROLE in member.roles and member.id not in top_1_ids:
            await member.remove_roles(Config.TOP_1_ROLE)

        # Top 3
        if member.id in top_3_ids and Config.TOP_3_ROLE not in member.roles:
            await member.add_roles(Config.TOP_3_ROLE)
        
        elif Config.TOP_3_ROLE in member.roles and member.id not in top_3_ids:
            await member.remove_roles(Config.TOP_3_ROLE)

        # Top 10
        if member.id in top_10_ids and Config.TOP_10_ROLE not in member.roles:
            await member.add_roles(Config.TOP_10_ROLE)
        
        elif Config.TOP_10_ROLE in member.roles and member.id not in top_10_ids:
            await member.remove_roles(Config.TOP_10_ROLE)

