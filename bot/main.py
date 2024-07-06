import discord
from misc.config import Config

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    Config.add_context(bot)
    bot.load_extension('cogs.channels')
    bot.load_extension('cogs.usernames')


bot.load_extension('cogs.commands')
bot.run(Config.TOKEN)