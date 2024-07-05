import discord

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    bot.load_extension('cogs.channels')
    bot.load_extension('cogs.usernames')


# Welcome message
@bot.event
async def on_member_join(member):
    welcome_channel_id = 1257178370408583288
    welcome_channel = bot.get_channel(welcome_channel_id)

    await welcome_channel.send(f"Hello {member.mention}!\n\nIf you haven't already, use the ``/username`` command to request a username so that you can use the server")


bot.load_extension('cogs.commands')
bot.run('MTI1NDY2NzUyMjMzMTExNTYwMQ.GbxCXq._Dhwg0c_jrh1LWiMKCVHSKziit-f0OoLMzRJfU')