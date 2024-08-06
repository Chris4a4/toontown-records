import discord

from singletons.config import Config
from singletons.channel_managers import ChannelManagers

from misc.rate_limited_bot import RateLimitedBot

bot = RateLimitedBot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    if not Config.DONE_LOADING:
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
        print('------')

        Config.add_context(bot)
        ChannelManagers.initialize(bot)
        bot.load_extension('cogs.force_update')  # This cog has to be loaded AFTER the bot knows which guilds its in


bot.load_extension('cogs.commands')  # These cogs have to be loaded BEFORE bot.run in order to be registered with discord correctly
bot.load_extension('cogs.events')
bot.run(Config.TOKEN)