import discord
from discord.ext import commands
from misc.config import Config

bot = commands.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    Config.add_context(bot)
    bot.load_extension('cogs.channels')  # These cogs have to be loaded AFTER the bot knows which guilds its in
    bot.load_extension('cogs.usernames')


bot.load_extension('cogs.commands')  # These cogs have to be loaded BEFORE bot.run in order to be registered with discord correctly
bot.load_extension('cogs.webhooks')
bot.run(Config.TOKEN)