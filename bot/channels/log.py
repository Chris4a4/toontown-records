from visuals.namechange import namechange_embed
from visuals.submission import submission_embed

from misc.auto_channel import AutoChannel
from misc.api_wrapper import get_logs


class LogChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        result = []
        for log in get_logs():
            if log['type'] == 'namechange':
                embed = namechange_embed(log['document'])
            else:
                embed = submission_embed(log['document'], 'logs')
            
            modification_msg = history_to_string(log['modifications'])

            result.append((modification_msg, embed, None, []))

        await self.auto_channel.apply(result)


def history_to_string(modifications):
    content = []

    for modification in modifications[::-1]:
        new_string = f'<@{modification['audit_id']}> used ``{modification['operation']}`` <t:{modification['timestamp']}:R>'

        if modification['operation'] == 'edit_record':
            edit_fields = []
            for key, value in modification['additional_info'].items():
                edit_fields.append(f'{key}: {value}')

            new_string += f'\n```{'\n'.join(edit_fields)}```'
        
        # Check that adding the next edit history item won't make the message too long
        if len('\n'.join(content)) + len(new_string) < 1900:
            content.insert(0, new_string)
        else:
            break
    
    return '\n'.join(content)