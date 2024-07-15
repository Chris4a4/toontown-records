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
    RATE_LIMIT_MESSAGE = 0
    RATE_LIMIT_GLOBAL = 0
    PERSONAL_LEADERBOARD_SIZE = 0

    SUBMIT_CHANNEL_ID = 0
    WELCOME_CHANNEL_ID = 0
    UPDATE_CHANNEL = 0
    WEBHOOK_CHANNEL_ID = 0
    GUILD = 0
    AUTHORIZED_ROLE = ''
    TOP_1_ROLE = ''
    TOP_3_ROLE = ''
    TOP_10_ROLE = ''
    TOKEN = ''

    # Populated after the bot is loaded
    @classmethod
    def add_context(cls, bot):
        cls.GUILD = bot.get_guild(cls.GUILD)
        cls.UPDATE_CHANNEL = bot.get_channel(cls.UPDATE_CHANNEL)
        cls.AUTHORIZED_ROLE = discord.utils.get(cls.GUILD.roles, name=cls.AUTHORIZED_ROLE)
        cls.TOP_1_ROLE = discord.utils.get(cls.GUILD.roles, name=cls.TOP_1_ROLE)
        cls.TOP_3_ROLE = discord.utils.get(cls.GUILD.roles, name=cls.TOP_3_ROLE)
        cls.TOP_10_ROLE = discord.utils.get(cls.GUILD.roles, name=cls.TOP_10_ROLE)

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
            cls.RATE_LIMIT_MESSAGE = data['RATE_LIMIT_MESSAGE']
            cls.RATE_LIMIT_GLOBAL = data['RATE_LIMIT_GLOBAL']
            cls.RECORD_CHANNELS = data['RECORD_CHANNELS']
            cls.LEADERBOARDS = data['LEADERBOARDS']
            cls.PERSONAL_LEADERBOARD_SIZE = data['PERSONAL_LEADERBOARD_SIZE']
    
    @classmethod
    def private_config(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            
            cls.UPDATE_CHANNEL = data['UPDATE_CHANNEL']
            cls.WEBHOOK_CHANNEL_ID = data['WEBHOOK_CHANNEL_ID']
            cls.SUBMIT_CHANNEL_ID = data['SUBMIT_CHANNEL_ID']
            cls.WELCOME_CHANNEL_ID = data['WELCOME_CHANNEL_ID']
            cls.GUILD = data['GUILD']
            cls.AUTHORIZED_ROLE = data['AUTHORIZED_ROLE']
            cls.TOP_1_ROLE = data['TOP_1_ROLE']
            cls.TOP_3_ROLE = data['TOP_3_ROLE']
            cls.TOP_10_ROLE = data['TOP_10_ROLE']
            cls.TOKEN = data['TOKEN']


public_path = os.path.join(os.path.dirname(__file__), '..',  'public_config.yaml')
Config.public_config(public_path)

private_path = os.path.join(os.path.dirname(__file__), '..',  'private_config.yaml')
Config.private_config(private_path)