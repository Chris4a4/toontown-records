import discord
from misc.config import Config

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    Config.add_context(bot)
    bot.load_extension('cogs.channels')
    bot.load_extension('cogs.usernames')


# Welcome message
@bot.event
async def on_member_join(member):
    await Config.WELCOME_CHANNEL.send(f'Hello {member.mention}!\n\nIf you have not already, use the ``/username`` command to request a username so that you can use the server')


bot.load_extension('cogs.commands')
bot.run(Config.TOKEN)