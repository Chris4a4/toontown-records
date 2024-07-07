from channels.leaderboard_channel import LeaderboardChannelManager
from channels.log_channel import LogChannelManager
from channels.namechange_channel import NamechangeChannelManager
from channels.records_channel import RecordChannelManager
from channels.submissions_channel import SubmissionsChannelManager
from channels.user_action_channel import UserActionChannelManager


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
        cls.record_channels = [
            RecordChannelManager(bot, 'ttr', 'vp'),
            RecordChannelManager(bot, 'ttr', 'cfo'),
            RecordChannelManager(bot, 'ttr', 'cj'),
            RecordChannelManager(bot, 'ttr', 'ceo'),
            RecordChannelManager(bot, 'ttr', 'activities')
        ]
        cls.leaderboard_channels = [
            LeaderboardChannelManager(bot, 'leaderboards', 'ttr'),
            LeaderboardChannelManager(bot, 'leaderboards', 'ttcc'),
            LeaderboardChannelManager(bot, 'leaderboards', 'overall')
        ]

        # Mod channels
        cls.namechange_channel = [NamechangeChannelManager(bot, 'staff', 'pending-namechanges')]
        cls.submission_channel = [SubmissionsChannelManager(bot, 'staff', 'pending-records')]
        cls.log_channel = [LogChannelManager(bot, 'staff', 'logs')]

    @classmethod
    async def force_update_all(cls):
        all_channels = cls.user_action_channel + cls.record_channels + cls.leaderboard_channels + cls.namechange_channel + cls.submission_channel + cls.log_channel

        for channel_manager in all_channels:
            await channel_manager.update()
    
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

        for channel_manager in channels_to_update:
            await channel_manager.update()
