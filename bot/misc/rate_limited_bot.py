from discord.ext import commands
import asyncio
from singletons.config import Config

# Wrap the normal bot class to include rate limiting on anything that needs it
class RateLimitedBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_limiter = MessageEditLimiter(self)

    async def edit_message(self, message, **kwargs):
        return await self.edit_limiter(message, **kwargs)

class MessageEditLimiter:
    def __init__(self, bot, interval=Config.RATE_LIMIT_INTERVAL):
        self.bot = bot
        self.interval = interval
        self.locks = {}

    # Only allow one edit on each message at a time + enforce a CD afterwards
    # Ideally would only process the most recent edit if multiple came in during CD, but that's so much extra complexity for no practical gain
    async def __call__(self, message, **kwargs):
        if not message.id in self.locks:
            self.locks[message.id] = asyncio.Lock()

        async with self.locks[message.id]:
            await message.edit(**kwargs)
            await asyncio.sleep(self.interval)