import discord


def namechange_embed(namechange):
    embed = discord.Embed(
        title=f'Name Change Request',
        description=f'<@{namechange['discord_id']}> wants to change their username from ``{namechange['current_username']}`` to ``{namechange['new_username']}``',
        color=discord.Colour.blurple()
    )

    # Raw data
    raw_data = []
    for key, value in namechange.items():
        raw_data.append(f'{key}: {value}')
    embed.add_field(name='Raw Data:', value=f'```{'\n'.join(raw_data)}```', inline=False)

    return embed