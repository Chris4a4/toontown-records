import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command()
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Modal via Slash Command")
    await ctx.send_modal(modal)

async def list_search(ctx: discord.AutocompleteContext):
    """Return's A List Of Autocomplete Results"""
    print('asdf')
    return ['a', 'b', 'c', 'd'] # from your database

@bot.slash_command(name="testy", description="TESTY")
async def set_embed_field(ctx: discord.ApplicationContext, 
                          person_1: discord.Option(str, required=False, autocomplete=list_search),
                          person_2: discord.Option(str, required=False, autocomplete=list_search),
                          person_3: discord.Option(str, required=False, autocomplete=list_search),
                          person_4: discord.Option(str, required=False, autocomplete=list_search),
                          person_5: discord.Option(str, required=False, autocomplete=list_search),
                          person_6: discord.Option(str, required=False, autocomplete=list_search),
                          person_7: discord.Option(str, required=False, autocomplete=list_search),
                          person_8: discord.Option(str, required=False, autocomplete=list_search)):
    await ctx.respond('a', emphemeral=True)

@bot.slash_command(name="create_embed", description="Create a blank embed")
async def create_embed(ctx: discord.ApplicationContext):
    embed = discord.Embed(title='a', description='b')

    message = await ctx.send(embed=embed)
    bot.embed_message = message

    await ctx.respond("Blank embed created! Use `/set_embed_field` to populate it.")

@bot.slash_command(name="set_embed_field", description="Set a field in the embed")
async def set_embed_field(ctx: discord.ApplicationContext, 
                          field_name: str, 
                          field_value: str):
    if hasattr(bot, 'embed_message'):
        embed = bot.embed_message.embeds[0]
        embed.add_field(name=field_name, value=field_value, inline=False)
        await bot.embed_message.edit(embed=embed)
        await ctx.response.defer()

        #await ctx.respond(f"Field '{field_name}' set to '{field_value}'!", ephemeral=True)
    else:
        await ctx.respond("No embed has been created yet. Use `/create_embed` first.", ephemeral=True)

# Define a command with a button
@bot.slash_command(name="button")
async def button_command(ctx):
    # Create a button
    class MyView(discord.ui.View):
        @discord.ui.button(label="Click me", style=discord.ButtonStyle.primary)
        async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Send another message when the button is clicked
            #await interaction.response.send_message("Button clicked!")
            #interaction.response.is_done = True
            await interaction.response.defer()
            await interaction.user.send('poop')
        @discord.ui.select( # the decorator that lets you specify the properties of the select menu
            placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = 3, # the maximum number of values that can be selected by the users
            options = [ # the list of options from which users can choose, a required field
                discord.SelectOption(
                    label="Vanilla",
                    description="Pick this if you like vanilla!"
                ),
                discord.SelectOption(
                    label="Chocolate",
                    description="Pick this if you like chocolate!"
                ),
                discord.SelectOption(
                    label="Strawberry",
                    description="Pick this if you like strawberry!"
                )
            ]
        )
        async def select_callback(self, select, interaction): # the function called when the user is done selecting options
            await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")


    # Send a message with the button
    await ctx.respond("Here is a button:", view=MyView())

bot.run('MTI1NDY2NzUyMjMzMTExNTYwMQ.GbxCXq._Dhwg0c_jrh1LWiMKCVHSKziit-f0OoLMzRJfU')