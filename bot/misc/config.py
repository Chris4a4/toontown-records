import yaml
import os
import discord

class Config:
    BASE_URL = ''
    UNKNOWN_THUMBNAIL = ''
    LEADERBOARD_TOP_N = 0
    TTR_ICON = ''
    TTR_COLOR = 0
    TTCC_ICON = ''
    TTCC_COLOR = 0
    OVERALL_ICON = ''
    OVERALL_COLOR = 0
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
    def public_config(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)

            cls.BASE_URL = data['BASE_URL']
            cls.UNKNOWN_THUMBNAIL = data['UNKNOWN_THUMBNAIL']
            cls.LEADERBOARD_TOP_N = data['LEADERBOARD_TOP_N']
            cls.TTR_ICON = data['TTR_ICON']
            cls.TTR_COLOR = data['TTR_COLOR']
            cls.TTCC_ICON = data['TTCC_ICON']
            cls.TTCC_COLOR = data['TTCC_COLOR']
            cls.OVERALL_ICON = data['OVERALL_ICON']
            cls.OVERALL_COLOR = data['OVERALL_COLOR']

    
    @classmethod
    def private_config(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            
            cls.WELCOME_CHANNEL = data['WELCOME_CHANNEL']
            cls.GUILD = data['GUILD']
            cls.AUTHORIZED_ROLE = data['AUTHORIZED_ROLE']
            cls.TOKEN = data['TOKEN']


public_path = os.path.join(os.path.dirname(__file__), '..',  'public_config.yaml')
Config.public_config(public_path)

private_path = os.path.join(os.path.dirname(__file__), '..',  'private_config.yaml')
Config.private_config(private_path)