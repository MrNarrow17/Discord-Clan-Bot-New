import discord


def send_roster(
    interaction: discord.Interaction, rosterchannel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="⭕ Send roster command was used",
        description=f"{interaction.user.mention} sent roster to {rosterchannel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def update_roster(
    interaction: discord.Interaction, rosterchannel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="⭕ Update roster command was used",
        description=f"{interaction.user.mention} updated roster in {rosterchannel.mention}",
        color=discord.Color.blue(),
    )

    return embed
