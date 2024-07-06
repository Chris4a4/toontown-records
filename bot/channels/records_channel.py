from misc.record_metadata import get_metadata, group_records, get_banner
from embeds.records_embed import records_embed
from channels.auto_channel import AutoChannel
import discord
from misc.api_wrapper import get_all_records


class RecordChannelManager:
    def __init__(self, bot, game, channel):
        self.bot = bot
        self.tags = [game, channel]
        self.auto_channel = AutoChannel(bot, game, channel)
    
    async def update(self):
        matching_records = []
        for record in get_all_records():
            if set(record['tags']) == set(self.tags) | set(record['tags']):
                matching_records.append(record)

        result = []
        for records in group_records(matching_records).values():
            embed = records_embed(records)

            category, thumbnail, color, banner_color = get_metadata(records[0]['tags'])

            file = get_banner(category, banner_color)

            result.append(('', embed, SubmitView(records), [file]))

        await self.auto_channel.apply(result)


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

                await interaction.response.send_message(f'```{submit_string}```', ephemeral=True)
                break
