import requests
from embeds.leaderboard_embed import leaderboard_embed
from channels.auto_channel import AutoChannel

class LeaderboardChannelManager:
    def __init__(self, bot, category, game):
        self.bot = bot
        self.game = game
        self.auto_channel = AutoChannel(bot, category, game)

    async def update(self):
        leaderboard_data = requests.get(f'http://backend:8000/api/records/get_leaderboard/{self.game}').json()

        embed = leaderboard_embed(leaderboard_data, self.game)

        await self.auto_channel.apply([('', embed, None, [])])