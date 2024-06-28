import discord

bot = discord.Bot()

async def list_search(ctx: discord.AutocompleteContext):
    """Return's A List Of Autocomplete Results"""
    return ['a', 'b', 'c'] # from your database
    
    
@bot.slash_command(name="ac_example")
async def autocomplete_example(
    ctx: discord.ApplicationContext,
    choice: discord.Option(str, "what will be your choice!", autocomplete=list_search),
):
    await ctx.respond(f"You picked {choice}!")

async def list_search(ctx: discord.AutocompleteContext):
    """Return's A List Of Autocomplete Results"""
    return [discord.OptionChoice('poop'), discord.OptionChoice('nug')] # from your database

@bot.slash_command(name="asdf")
async def asdf(
    ctx: discord.ApplicationContext,
    choice: discord.Option(str, "what will be your choice!", autocomplete=list_search), # type: ignore
):
    await ctx.respond(f"You picked {choice}!")

account_choices = {
    "GIM": "gim",
    "Main": "main",
    "UIM": "uim"
}
@bot.slash_command(name="kruk", description="Shows my Kruk dungeon path for my OSRS accounts")
async def kruk(ctx, account: discord.Option(str, "Which account", choices=list(account_choices.keys()), required=True)): # type: ignore
    # Get the corresponding value from the chosen display name
    account_value = account_choices[account]
    await ctx.respond(f'Selected account: {account_value}', ephemeral=True)

@bot.user_command(name="Account Creation Date")  # create a user command for the supplied guilds
async def account_creation_date(ctx, member: discord.Member):  # user commands return the member
    await ctx.respond(f"{member.name}'s account was created on {member.created_at}")

@bot.message_command(name="Get Message ID")  # creates a global message command. use guild_ids=[] to create guild-specific commands.
async def get_message_id(ctx, message: discord.Message):  # message commands return the message
    await ctx.respond(f"Message ID: `{message.id}`")

bot.run('MTI1NDY2NzUyMjMzMTExNTYwMQ.GbxCXq._Dhwg0c_jrh1LWiMKCVHSKziit-f0OoLMzRJfU')