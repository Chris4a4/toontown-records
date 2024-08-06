import discord
from discord.ext import commands

from singletons.config import Config
from singletons.channel_managers import ChannelManagers

from misc.rate_limited_bot import RateLimitedBot

bot = RateLimitedBot(intents=discord.Intents.all())

first_load = True

@bot.event
async def on_ready():
    if first_load:
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
        print('------')

        Config.add_context(bot)
        ChannelManagers.initialize(bot)
        bot.load_extension('cogs.force_update')  # This cog has to be loaded AFTER the bot knows which guilds its in

        first_load = False


bot.load_extension('cogs.commands')  # These cogs have to be loaded BEFORE bot.run in order to be registered with discord correctly
bot.load_extension('cogs.events')
bot.run(Config.TOKEN)