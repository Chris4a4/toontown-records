from misc.record_metadata import get_metadata, group_records, get_banner
from visuals.records import records_embed
from misc.auto_channel import AutoChannel
import discord
from misc.api_wrapper import get_records_with_tags
from singletons.config import Config


class RecordChannelManager:
    def __init__(self, bot, game, channel):
        self.bot = bot
        self.tags = [game, channel]
        self.auto_channel = AutoChannel(bot, game, channel)
    
    async def update(self):
        content = []
        for records in group_records(get_records_with_tags(self.tags)).values():
            embed = records_embed(records)

            category, thumbnail, color, banner_color = get_metadata(records[0]['tags'])

            file = get_banner(category, banner_color)

            content.append(('', embed, SubmitView(records), [file]))

        await self.auto_channel.update_all(content)
    
    # Calls update if any of the records given match this channel
    async def update_if_matches(self, record_names):
        for record in get_records_with_tags(self.tags):
            if record['record_name'] in record_names:
                await self.update()
                return


class SubmitView(discord.ui.View):
    def __init__(self, records):
        super().__init__(timeout=None)
        self.records = records

        options = []
        for record in records:
            if record['max_players'] == 1:
                players_string = '1'
            else:
                players_string = f'1 - {record['max_players']}'
            
            must_submit = []
            if record['time_required']:
                must_submit.append('Time')
            if record['score_required']:
                must_submit.append('Score')

            desc = f'Valid players: {players_string} | Must submit: {' & '.join(must_submit)}'

            options.append(discord.SelectOption(label=record['record_name'], description=desc))
        
        self.select_menu = discord.ui.Select(placeholder='Submit a record', min_values=1, max_values=1, options=options)
        self.select_menu.callback = self.select_callback
    
        self.add_item(self.select_menu)

    async def select_callback(self, interaction):
        base_text = f'Copy the command below, and go to <#{Config.SUBMIT_CHANNEL_ID}> to submit your record:'

        selected_record = self.select_menu.values[0]

        for record in self.records:
            record_name = record['record_name']

            if record_name == selected_record:
                submit_string = f'/submit record:{record_name} evidence: '

                if record['time_required']:
                    submit_string += 'time: '
                if record['score_required']:
                    submit_string += 'score: '
                
                for i in range(0, record['max_players']):
                    submit_string += f'user{i + 1}: '

                await interaction.response.send_message(f'{base_text}', ephemeral=True)
                await interaction.followup.send(f'```{submit_string}```', ephemeral=True)
                break
