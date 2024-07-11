from channels.leaderboard_channel import LeaderboardChannelManager
from channels.log_channel import LogChannelManager
from channels.namechange_channel import NamechangeChannelManager
from channels.records_channel import RecordChannelManager
from channels.submissions_channel import SubmissionsChannelManager
from channels.user_action_channel import UserActionChannelManager

from singletons.config import Config

from asyncio import TaskGroup


class ChannelManagers:
    # Public channels
    user_action_channel = []
    record_channels = []
    leaderboard_channels = []

    # Mod channels
    namechange_channel = []
    submission_channel = []
    log_channel = []

    # Populated after the bot is loaded
    @classmethod
    def initialize(cls, bot):
        # Public channels
        cls.user_action_channel = [UserActionChannelManager(bot, 'submissions and requests', 'user-guide')]
        cls.record_channels = [RecordChannelManager(bot, *info) for info in Config.RECORD_CHANNELS]
        cls.leaderboard_channels = [RecordChannelManager(bot, 'leaderboards', game) for game in Config.LEADERBOARDS]

        # Mod channels
        cls.namechange_channel = [NamechangeChannelManager(bot, 'staff', 'pending-namechanges')]
        cls.submission_channel = [SubmissionsChannelManager(bot, 'staff', 'pending-records')]
        cls.log_channel = [LogChannelManager(bot, 'staff', 'logs')]

    @classmethod
    async def force_update_all(cls):
        all_channels = cls.user_action_channel + cls.record_channels + cls.leaderboard_channels + cls.namechange_channel + cls.submission_channel + cls.log_channel

        async with TaskGroup() as tg:
            for channel_manager in all_channels:
                tg.create_task(channel_manager.update())
    
    @classmethod
    async def update_from_function(cls, function_name):
        update_schema = {
            'submit': cls.submission_channel,
            'edit_submission': cls.submission_channel,
            'approve_submission': cls.record_channels + cls.leaderboard_channels,
            'deny_submission': [],
            'request_namechange': cls.namechange_channel,
            'approve_namechange': cls.record_channels + cls.leaderboard_channels,
            'deny_namechange': [],
            'obsolete_namechange': []
        }
        channels_to_update = update_schema[function_name] + cls.log_channel  # Always update the log channel

        async with TaskGroup() as tg:
            for channel_manager in channels_to_update:
                tg.create_task(channel_manager.update())
