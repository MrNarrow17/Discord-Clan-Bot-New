import discord


def say(interaction: discord.Interaction) -> discord.Embed:
    if isinstance(interaction.channel, discord.TextChannel):
        channel_mention = interaction.channel.mention
    else:
        channel_mention = "unknown channel"

    embed = discord.Embed(
        title="🔊 Say command was used",
        description=f"{interaction.user.mention} used the say command in {channel_mention}",
        color=discord.Color.blue(),
    )

    return embed


def embed(interaction: discord.Interaction) -> discord.Embed:
    if isinstance(interaction.channel, discord.TextChannel):
        channel_mention = interaction.channel.mention
    else:
        channel_mention = "unknown channel"

    embed = discord.Embed(
        title="🤖 Embed command was used",
        description=f"{interaction.user.mention} sent and embed to {channel_mention}",
        color=discord.Color.blue(),
    )

    return embed


def ping(interaction: discord.Interaction, latency: str) -> discord.Embed:
    embed = discord.Embed(
        title="🏓 Ping command was used",
        description=f"{interaction.user.mention} pinged the bot, latency was {latency}ms",
        color=discord.Color.blue(),
    )

    return embed
