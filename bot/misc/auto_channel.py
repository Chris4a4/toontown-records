import re
import discord

from singletons.config import Config
from asyncio import TaskGroup


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

        async with TaskGroup() as tg:
            for desired_content in desired_contents:
                content, embed, view, files = desired_content
                message = await anext(iter)

                if (self.first_load and view) or has_changed(message, content, embed, view, files):
                    tg.create_task(self.bot.edit_message(message, content=content, embed=embed, view=view, attachments=[], files=files))

        await iter.aclose()

        self.first_load = False

    # Gets a category by name, if it exists. Otherwise creates it
    async def get_category(self, desired_category):
        for category in Config.GUILD.categories:
            if category.name == desired_category:
                return category

        return await Config.GUILD.create_category(desired_category)

    # Gets a channel by name + category name, if it exists. Otherwise creates it
    async def get_channel(self, desired_category, desired_channel):
        category = await self.get_category(desired_category)

        actual_name = re.sub(r'[^A-Za-z0-9 _\-]', '', desired_channel.lower().replace(' ', '-'))
        for channel in Config.GUILD.channels:
            if channel.category == category and channel.name == actual_name:
                return channel

        return await Config.GUILD.create_text_channel(actual_name, category=category)

    # Constructs a message iterator for the specified channel
    async def get_iterator(self):
        channel = await self.get_channel(self.category, self.channel)
        temp_history = await channel.history(oldest_first=True).flatten()

        # Delete all non-bot messages and gather what's left
        history = []
        for msg in temp_history:
            if not msg.author.id == self.bot.user.id:
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
        for msg in self.history:
            try:
                await msg.delete()
            except discord.NotFound:
                pass
