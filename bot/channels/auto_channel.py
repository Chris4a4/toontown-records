import re
import discord


# Compares message's content to the new content
def has_changed(message, new_text, new_embed, new_view, new_files):
    # Gather original message contents
    cur_message = {'msg': message.content}

    if message.embeds:
        current_embed = message.embeds[0].to_dict()
        if 'thumbnail' in current_embed:  # Remove the extra metadata discord adds before comparison
            if 'proxy_url' in current_embed['thumbnail']:
                del current_embed['thumbnail']['proxy_url']
            if 'width' in current_embed['thumbnail']:
                del current_embed['thumbnail']['width']
            if 'height' in current_embed['thumbnail']:
                del current_embed['thumbnail']['height']
        cur_message['embed'] = current_embed

    if message.components:
        cur_view = discord.ui.View.from_message(message)
        cur_message['view'] = str(cur_view.children)
    
    if message.attachments:
        cur_message['file'] = message.attachments[0].filename

    # Gather new message contents
    new_message = {'msg': new_text}
    if new_embed:
        new_message['embed'] = new_embed.to_dict()

    if new_view:
        new_message['view'] = str(new_view.children)
    
    if new_files:
        new_message['file'] = new_files[0].filename

    if cur_message != new_message:
        print('MESSAGE DIFFERENT')
        print(cur_message)
        print(new_message)
        print()

    # Compare contents and edit if necessary
    return cur_message != new_message


class AutoChannel:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.category = category
        self.channel = channel
        self.first_load = True

    # Takes in a list of (content, embed, view, file) pairs and populates the channel with them IN ORDER GIVEN
    async def apply(self, desired_contents):
        iter = await self.get_iterator()
        
        for desired_content in desired_contents:
            content, embed, view, files = desired_content
            message = await anext(iter)

            if (self.first_load and view) or has_changed(message, content, embed, view, files):
                await message.edit(content=content, embed=embed, view=view, attachments=[], files=files)
        
        await iter.aclose()
        
        self.first_load = False

    # Gets the record bot's associated discord server object
    # Throws an error if the bot is not in exactly one server
    def get_guild(self):
        guilds = self.bot.guilds

        if len(guilds) > 1:
            print('ERROR: Bot is in more than one discord server')
        elif len(guilds) == 0:
            print('ERROR: Bot is not in a discord server')
        else:
            return guilds[0]

    # Gets a category by name, if it exists. Otherwise creates it
    async def get_category(self, desired_category):
        for category in self.get_guild().categories:
            if category.name == desired_category:
                return category

        print(f'WARNING: Category {desired_category} did not exist')
        return await self.get_guild().create_category(desired_category)

    # Gets a channel by name + category name, if it exists. Otherwise creates it
    async def get_channel(self, desired_category, desired_channel):
        category = await self.get_category(desired_category)

        actual_name = re.sub(r'[^A-Za-z0-9 _\-]', '', desired_channel.lower().replace(' ', '-'))
        for channel in self.get_guild().channels:
            if channel.category == category and channel.name == actual_name:
                return channel

        print(f'WARNING: Channel {desired_category}/#{actual_name} did not exist')
        return await self.get_guild().create_text_channel(actual_name, category=category)

    # Constructs a message iterator for the specified channel
    async def get_iterator(self):
        channel = await self.get_channel(self.category, self.channel)
        temp_history = await channel.history(oldest_first=True).flatten()

        # Delete all non-bot messages and gather what's left
        history = []
        for msg in temp_history:
            if not msg.author.id == self.bot.user.id:
                print(f'WARNING: Message from {str(msg.author)} was in bot-only channel #{channel.name}')
                await msg.delete()
            else:
                history.append(msg)

        return MessageIterator(channel, history)


# Abstracts organizing a channel as a series of next() functions which each return the next message in the channel
class MessageIterator:
    def __init__(self, channel, history):
        self.channel = channel
        self.history = history

    async def __aiter__(self):
        return self

    # Either return the next message in the history or create one and return it
    async def __anext__(self):
        if len(self.history) > 0:
            return self.history.pop(0)

        return await self.channel.send(content='...')

    # Delete all the remaining messages
    async def aclose(self):
        if len(self.history) > 0:
            print(f'WARNING: Deleted {len(self.history)} extra messages in channel #{self.channel.name}')

        for msg in self.history:
            await msg.delete()
