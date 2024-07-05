import yaml
import os
import discord

class Config:
    BASE_URL = ''
    UNKNOWN_THUMBNAIL = ''
    LEADERBOARD_TOP_N = 0
    WELCOME_CHANNEL = 0
    GUILD = 0
    AUTHORIZED_ROLE = ''
    TOKEN = ''

    # Populated after the bot is loaded
    @classmethod
    def add_context(cls, bot):
        cls.GUILD = bot.get_guild(cls.GUILD)
        cls.WELCOME_CHANNEL = bot.get_channel(cls.WELCOME_CHANNEL)
        cls.AUTHORIZED_ROLE = discord.utils.get(cls.GUILD.roles, name=cls.AUTHORIZED_ROLE)

    # Can be populated immediately
    @classmethod
    def load_from_file(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)

            cls.BASE_URL = data['BASE_URL']
            cls.UNKNOWN_THUMBNAIL = data['UNKNOWN_THUMBNAIL']
            cls.LEADERBOARD_TOP_N = data['LEADERBOARD_TOP_N']
            cls.WELCOME_CHANNEL = data['WELCOME_CHANNEL']
            cls.GUILD = data['GUILD']
            cls.AUTHORIZED_ROLE = data['AUTHORIZED_ROLE']
            cls.TOKEN = data['TOKEN']

config_path = os.path.join(os.path.dirname(__file__), '..',  'config.yaml')
Config.load_from_file(config_path)