from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from discord import app_commands

from bot import purge_group
from settings import settings
from tools.fetch import Fetch
from tools.logembeds import moderation as logging
from tools.ui import ContactSupportView


def setup(tree, bot):
    fetch = Fetch(bot)

    @purge_group.command(
        name="all", description="Purge all messages in specific channel"
    )
    @app_commands.describe(
        channel="Choose what channel to purge in",
        amount="How many messages",
    )
    async def purge_all(
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        amount: int,
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        if amount > 100:
            await interaction.followup.send(
                "Cannot purge more than 100 messages!", ephemeral=True
            )
            return

        messages = await fetch.fetch_messages(channel, amount)

        fourteen_days_ago = datetime.now(timezone.utc) - timedelta(days=14)
        bulk_deletable = [m for m in messages if m.created_at > fourteen_days_ago]
        old_messages = [m for m in messages if m.created_at <= fourteen_days_ago]

        deleted_count = 0

        if bulk_deletable:
            try:
                await channel.delete_messages(bulk_deletable)
                deleted_count += len(bulk_deletable)
            except discord.Forbidden:
                pass
            except discord.HTTPException:
                for msg in bulk_deletable:
                    try:
                        await msg.delete()
                        deleted_count += 1
                    except (
                        discord.Forbidden,
                        discord.NotFound,
                        discord.HTTPException,
                    ):
                        continue

        for msg in old_messages:
            try:
                await msg.delete()
                deleted_count += 1
            except (
                discord.Forbidden,
                discord.NotFound,
                discord.HTTPException,
            ):
                continue

        await interaction.followup.send(
            f"Deleted {deleted_count}/{len(messages)} messages.",
            ephemeral=True,
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.purge_all(interaction, channel, amount))

    @tree.command(
        name="warn",
        description="Warn a user",
    )
    @app_commands.describe(
        user="Who to warn",
        reason="Text to warn the user",
        anonymous="Whether to send the warning anonymously",
    )
    async def warn(
        interaction: discord.Interaction,
        user: discord.User,
        reason: Optional[str] = None,
        anonymous: bool = True,
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        if user.bot:
            await interaction.followup.send("You can't warn a bot!", ephemeral=True)
        else:
            try:
                embed = discord.Embed(
                    title="⚔️ Member Warning",
                    description=(
                        f"```\n  Server: {guild or 'Unknown Server'}  ·  Action: Warning\n```"
                    ),
                    color=0xED4245,
                    timestamp=discord.utils.utcnow(),
                )

                embed.add_field(
                    name="▸ 📋 Details",
                    value=(
                        f"> `🏠` **Server** ─ **{guild}**\n"
                        + (
                            f"> `🛡` **Issued by** ─ {interaction.user.mention}\n"
                            if not anonymous
                            else ""
                        )
                    )
                    + "\u200b",
                    inline=False,
                )

                embed.add_field(
                    name="▸ 📝 Reason",
                    value=f"> {reason}\n\u200b"
                    if reason
                    else "> *No reason provided.*\n\u200b",
                    inline=False,
                )

                embed.set_footer(
                    text=f"🏠 {guild or 'Unknown Server'} • Warning issued",
                )

                supportrole = settings.read_settings(guild, "supportrole")

                if supportrole:
                    view = ContactSupportView(guild.id)
                    await user.send(embed=embed, view=view)
                else:
                    await user.send(embed=embed)

                await interaction.followup.send(
                    f"Warned {user.mention}!", ephemeral=True
                )

                logchannel_id = settings.read_settings(guild, "logchannel")
                logchannel = guild.get_channel(logchannel_id)
                if isinstance(logchannel, discord.TextChannel):
                    await logchannel.send(embed=logging.warn(interaction, user, reason))

            except discord.Forbidden:
                await interaction.followup.send(
                    "Could not warn! The user might have DMs disabled.",
                    ephemeral=True,
                )
            except Exception as e:
                await interaction.followup.send(
                    f"An error occurred: {e}",
                    ephemeral=True,
                )

    @tree.command(name="timeout", description="Timeout someone for some time")
    @app_commands.describe(
        member="Who to timeout",
        minutes="How long to timeout in minutes",
        reason="Reason of timeout",
        anonymous="Whether to send the info anonymously",
    )
    async def timeout(
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: Optional[str] = None,
        anonymous: bool = False,
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)

        if minutes <= 0:
            await interaction.followup.send("Invalid time!", ephemeral=True)
            return
        duration = timedelta(minutes=minutes)

        if member.bot:
            await interaction.followup.send("You can't timeout a bot!", ephemeral=True)
            return

        try:
            if member.timed_out_until and member.timed_out_until > datetime.now(
                timezone.utc
            ):
                await member.timeout(None)
            await member.timeout(duration, reason=reason)
            await interaction.followup.send(
                f"Timed out {member.mention} for {minutes} minutes!",
                ephemeral=True,
            )

            try:
                embed = discord.Embed(
                    title="⚔️ Member Timeout",
                    description=(
                        f"```\n  Server: {guild or 'Unknown Server'}  ·  Duration: {minutes} minutes\n```"
                    ),
                    color=0xED4245,
                    timestamp=discord.utils.utcnow(),
                )

                embed.add_field(
                    name="▸ 📋 Details",
                    value=(
                        f"> `🏠` **Server** ─ **{guild}**\n"
                        f"> `⏱` **Duration** ─ **{minutes}** minutes\n"
                        + (
                            f"> `🛡` **Issued by** ─ {interaction.user.mention}\n"
                            if not anonymous
                            else ""
                        )
                    )
                    + "\u200b",
                    inline=False,
                )

                embed.add_field(
                    name="▸ 📝 Reason",
                    value=f"> {reason}\n\u200b"
                    if reason
                    else "> *No reason provided.*\n\u200b",
                    inline=False,
                )

                embed.set_footer(
                    text=f"🏠 {guild or 'Unknown Server'} • Timeout issued",
                )

                supportrole = settings.read_settings(guild, "supportrole")

                if supportrole:
                    view = ContactSupportView(guild.id)
                    await member.send(embed=embed, view=view)
                else:
                    await member.send(embed=embed)
                logchannel_id = settings.read_settings(guild, "logchannel")
                logchannel = guild.get_channel(logchannel_id)
                if isinstance(logchannel, discord.TextChannel):
                    await logchannel.send(
                        embed=logging.timeout(interaction, member, minutes, reason)
                    )

            except discord.Forbidden:
                await interaction.followup.send(
                    "Could not info them in DMs! The user might have DMs disabled.",
                    ephemeral=True,
                )
            except Exception as e:
                await interaction.followup.send(
                    f"An error occurred while sending the timeout message: {e}",
                    ephemeral=True,
                )

        except discord.Forbidden:
            await interaction.followup.send(
                "I don't have permission to timeout this user.",
                ephemeral=True,
            )

    @tree.command(name="untimeout", description="Remove the timeout from someone")
    @app_commands.describe(
        member="Who to timeout",
        reason="Reason of remove the timeout",
        anonymous="Whether to send the info anonymously",
    )
    async def untimeout(
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str] = None,
        anonymous: bool = False,
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)

        if member.bot:
            await interaction.followup.send(
                "You can't untimeout a bot!", ephemeral=True
            )
            return

        if member.timed_out_until and member.timed_out_until < datetime.now(
            timezone.utc
        ):
            await interaction.followup.send(
                "The user doesn't have a timeout!", ephemeral=True
            )
            return
        try:
            await member.timeout(None)

            try:
                embed = discord.Embed(
                    title="⚔️ Timeout Removed",
                    description=(
                        f"```\n  Server: {guild or 'Unknown Server'}  ·  Action: Timeout Lifted\n```"
                    ),
                    color=0x57F287,
                    timestamp=discord.utils.utcnow(),
                )

                embed.add_field(
                    name="▸ 📋 Details",
                    value=(
                        f"> `🏠` **Server** ─ **{guild}**\n"
                        + (
                            f"> `🛡` **Removed by** ─ {interaction.user.mention}\n"
                            if not anonymous
                            else ""
                        )
                    )
                    + "\u200b",
                    inline=False,
                )

                embed.add_field(
                    name="▸ 📝 Reason",
                    value=f"> {reason}\n\u200b"
                    if reason
                    else "> *No reason provided.*\n\u200b",
                    inline=False,
                )

                embed.set_footer(
                    text=f"🏠 {guild or 'Unknown Server'} • Timeout removed",
                )

                await member.send(embed=embed)

                logchannel_id = settings.read_settings(guild, "logchannel")
                logchannel = guild.get_channel(logchannel_id)
                if isinstance(logchannel, discord.TextChannel):
                    await logchannel.send(
                        embed=logging.untimeout(interaction, member, reason)
                    )

            except discord.Forbidden:
                await interaction.followup.send(
                    "Could not info them in DMs! The user might have DMs disabled.",
                    ephemeral=True,
                )
            except Exception as e:
                await interaction.followup.send(
                    f"An error occurred while sending the timeout message: {e}",
                    ephemeral=True,
                )

        except discord.Forbidden:
            await interaction.followup.send(
                "I don't have permission to timeout this user.",
                ephemeral=True,
            )
