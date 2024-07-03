import discord

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    bot.load_extension('cogs.channels')
    bot.load_extension('cogs.usernames')

bot.load_extension('cogs.commands')
bot.run('MTI1NDY2NzUyMjMzMTExNTYwMQ.GbxCXq._Dhwg0c_jrh1LWiMKCVHSKziit-f0OoLMzRJfU')