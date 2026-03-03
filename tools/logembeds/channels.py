import discord


def logchannel_set(
    interaction: discord.Interaction, log_channel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="🪵 Logging channel was set",
        description=f"{interaction.user.mention} set the logging channel to {log_channel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def supportchannel_set(
    interaction: discord.Interaction, log_channel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="🎫 Support channel was set",
        description=f"{interaction.user.mention} set the support channel to {log_channel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def supportchannel_remove(interaction: discord.Interaction) -> discord.Embed:

    embed = discord.Embed(
        title="🎫 Support channel was removed",
        description=f"{interaction.user.mention} removed the support channel",
        color=discord.Color.blue(),
    )

    return embed


def tryoutchannel_set(
    interaction: discord.Interaction, log_channel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Tryout channel was set",
        description=f"{interaction.user.mention} set the tryout channel to {log_channel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def tryoutchannel_remove(interaction: discord.Interaction) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Tryout channel was removed",
        description=f"{interaction.user.mention} removed the tryout channel",
        color=discord.Color.blue(),
    )

    return embed


def rosterchannel_set(
    interaction: discord.Interaction, log_channel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="⭕ Roster channel was set",
        description=f"{interaction.user.mention} set the roster channel to {log_channel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def rosterchannel_remove(interaction: discord.Interaction) -> discord.Embed:

    embed = discord.Embed(
        title="⭕ Roster channel was removed",
        description=f"{interaction.user.mention} removed the roster channel",
        color=discord.Color.blue(),
    )

    return embed
