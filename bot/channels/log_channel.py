import requests
from embeds.namechange_embed import namechange_embed
from embeds.submission_embed import submission_embed
from channels.auto_channel import AutoChannel

class LogChannelManager:
    def __init__(self, bot, category, channel):
        self.bot = bot
        self.auto_channel = AutoChannel(bot, category, channel)
    
    async def update(self):
        logs = requests.get(f'http://backend:8000/api/logging/get_logs').json()['data']

        result = []
        for log in logs:
            if log['type'] == 'namechange':
                embed = namechange_embed(log['document'])
            else:
                embed = submission_embed(log['document'])
            
            modification_msg = history_to_string(log['modifications'])

            result.append((modification_msg, embed, None, []))

        await self.auto_channel.apply(result)


def history_to_string(modifications):
    content = []

    for modification in modifications:
        content.append(f'<@{modification['audit_id']}> used ``{modification['operation']}`` <t:{modification['timestamp']}:R>')

        if modification['operation'] == 'edit_record':
            edit_fields = []
            for key, value in modification['additional_info'].items():
                edit_fields.append(f'{key}: {value}')

            content.append(f'```{'\n'.join(edit_fields)}```')
    
    return '\n'.join(content)