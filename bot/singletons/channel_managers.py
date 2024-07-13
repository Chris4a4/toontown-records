from channels.leaderboard import LeaderboardChannelManager
from channels.log import LogChannelManager
from channels.namechange import NamechangeChannelManager
from channels.records import RecordChannelManager
from channels.submissions import SubmissionsChannelManager
from channels.user_action import UserActionChannelManager

from singletons.config import Config
from misc.api_wrapper import get_approved_submissions

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
        cls.user_action_channel = UserActionChannelManager(bot, 'submissions and requests', 'user-guide')
        cls.record_channels = [RecordChannelManager(bot, *info) for info in Config.RECORD_CHANNELS]
        cls.leaderboard_channels = [LeaderboardChannelManager(bot, 'leaderboards', game) for game in Config.LEADERBOARDS]

        # Mod channels
        cls.namechange_channel = NamechangeChannelManager(bot, 'staff', 'pending-namechanges')
        cls.submission_channel = SubmissionsChannelManager(bot, 'staff', 'pending-records')
        cls.log_channel = LogChannelManager(bot, 'staff', 'logs')

    @classmethod
    async def force_update_all(cls):
        all_channels = [cls.user_action_channel] + cls.record_channels + cls.leaderboard_channels + [cls.namechange_channel] + [cls.submission_channel] + [cls.log_channel]

        async with TaskGroup() as tg:
            for channel_manager in all_channels:
                tg.create_task(channel_manager.update())
    
    @classmethod
    async def update_from_function(cls, function_name, params):
        async with TaskGroup() as tg:
            tg.create_task(cls.log_channel.update())

            match function_name:
                case 'submit':
                    tg.create_task(cls.submission_channel.update())
                
                case 'edit_submission':
                    if params['status'] == 'APPROVED':
                        tg.create_task(cls.update_leaderboards())
                        tg.create_task(cls.update_record_channels([params['record_name']]))
                    elif params['status'] == 'PENDING':
                        tg.create_task(cls.submission_channel.update())
                
                case 'approve_submission':
                    tg.create_task(cls.update_leaderboards())
                    tg.create_task(cls.update_record_channels([params['record_name']]))

                case 'deny_submission':
                    if params['status'] == 'APPROVED':
                        tg.create_task(cls.update_leaderboards())
                        tg.create_task(cls.update_record_channels([params['record_name']]))
                
                case 'request_namechange':
                    tg.create_task(cls.namechange_channel.update())
                
                case 'approve_namechange':
                    user_submissions = get_approved_submissions(params['discord_id'])
                    user_records = [submission['record_name'] for submission in user_submissions]

                    tg.create_task(cls.update_record_channels(user_records))

                case 'deny_namechange':
                    pass
    
    @classmethod
    async def update_leaderboards(cls):
        async with TaskGroup() as tg:
            for manager in cls.leaderboard_channels:
                tg.create_task(manager.update())
    
    @classmethod
    async def update_record_channels(cls, records):
        async with TaskGroup() as tg:
            for manager in cls.record_channels:
                tg.create_task(manager.update_if_matches(records))

