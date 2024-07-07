from embeds.leaderboard_embed import leaderboard_embed
from misc.auto_channel import AutoChannel

class LeaderboardChannelManager:
    def __init__(self, bot, category, game):
        self.bot = bot
        self.game = game
        self.auto_channel = AutoChannel(bot, category, game)

    async def update(self):
        embed = leaderboard_embed(self.game)

        await self.auto_channel.apply([('', embed, None, [])])