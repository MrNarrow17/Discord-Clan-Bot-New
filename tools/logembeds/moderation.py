from typing import Optional

import discord


def purge_all(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    amount: int,
) -> discord.Embed:

    embed = discord.Embed(
        title="🗑 Purge command was used",
        description=f"{interaction.user.mention} purged {amount} messages in {channel.mention}",
        color=discord.Color.blue(),
    )

    return embed


def warn(
    interaction: discord.Interaction,
    user: discord.User,
    reason: Optional[str] = None,
) -> discord.Embed:

    embed = discord.Embed(
        title="⚠️ Warn command was used",
        description=f"{interaction.user.mention} warned {user.mention}",
        color=discord.Color.blue(),
    )

    embed.add_field(name="Reason:", value=reason or "No reason provided")

    return embed


def timeout(
    interaction: discord.Interaction,
    member: discord.Member,
    time: int,
    reason: Optional[str] = None,
) -> discord.Embed:

    embed = discord.Embed(
        title="⏲️ Timeout command was used",
        description=f"{interaction.user.mention} timed out {member.mention} for {time}",
        color=discord.Color.blue(),
    )

    embed.add_field(name="Reason:", value=reason or "No reason provided")

    return embed


def untimeout(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: Optional[str] = None,
) -> discord.Embed:

    embed = discord.Embed(
        title="⏲️ Untimeout command was used",
        description=f"{interaction.user.mention} removed the timeout from {member.mention}",
        color=discord.Color.blue(),
    )

    embed.add_field(name="Reason:", value=reason or "No reason provided")

    return embed
