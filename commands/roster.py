import discord

from bot import roster_group
from settings import settings
from tools.embed_templates import roster_embed
from tools.fetch import Fetch
from tools.logembeds import roster as logging


def setup(tree, bot):
    fetch = Fetch(bot)

    @roster_group.command(name="send", description="Send roster")
    async def send_roster(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        member_role_id = settings.read_settings(guild, "memberrole")
        sub_member_role_id = settings.read_settings(guild, "submemberrole")
        roster_channel_id = settings.read_settings(guild, "rosterchannel")

        if not roster_channel_id:
            await interaction.followup.send(
                "Roster channel is not configured!", ephemeral=True
            )
            return

        roster_channel = guild.get_channel(roster_channel_id)

        if not isinstance(roster_channel, discord.TextChannel):
            await interaction.followup.send(
                "Roster channel is invalid!", ephemeral=True
            )
            return

        members = await fetch.fetch_members_with_role(guild, member_role_id)

        sub_members = await fetch.fetch_members_with_role(guild, sub_member_role_id)

        member_lines = [f"> {m.mention}" for m in members]
        sub_member_lines = [f"> {m.mention}" for m in sub_members]

        message = ""

        if member_lines:
            message += "**MEMBERS**\n"
            message += "\n".join(member_lines)

        if sub_member_lines:
            if message:
                message += "\n\n"
            message += "**SUBS**\n"
            message += "\n".join(sub_member_lines)

        if not message:
            await interaction.followup.send(
                "No members found for configured roles.", ephemeral=True
            )
            return

        if len("\n".join(f"> {m.mention}" for m in members)) > 1024:
            await interaction.followup.send(
                "Roster is too large to send in one message.", ephemeral=True
            )
            return

        embed = roster_embed(guild, members, sub_members)

        sent_message = await roster_channel.send(
            embed=embed, allowed_mentions=discord.AllowedMentions(users=True)
        )

        settings.write_settings(guild, "roster_message_id", sent_message.id)

        await interaction.followup.send(
            f"Roster sent to {roster_channel.mention}", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)

        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.send_roster(interaction, roster_channel)
            )

    @roster_group.command(name="update", description="Update roster message")
    async def update_roster(interaction: discord.Interaction):

        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        roster_channel_id = settings.read_settings(guild, "rosterchannel")
        roster_message_id = settings.read_settings(guild, "roster_message_id")

        if not roster_channel_id or not roster_message_id:
            await interaction.followup.send(
                "Roster message not found! Use /roster to send first.", ephemeral=True
            )
            return

        roster_channel = guild.get_channel(roster_channel_id)
        if not isinstance(roster_channel, discord.TextChannel):
            await interaction.followup.send("Roster channel invalid!", ephemeral=True)
            return

        try:
            roster_message = await roster_channel.fetch_message(roster_message_id)
        except discord.NotFound:
            await interaction.followup.send(
                "Roster message was deleted! Use /roster to send again.", ephemeral=True
            )
            return

        member_role_id = settings.read_settings(guild, "memberrole")
        sub_member_role_id = settings.read_settings(guild, "submemberrole")

        members = await fetch.fetch_members_with_role(guild, member_role_id)
        sub_members = await fetch.fetch_members_with_role(guild, sub_member_role_id)

        embed = roster_embed(guild, members, sub_members)

        await roster_message.edit(
            embed=embed, allowed_mentions=discord.AllowedMentions(users=True)
        )

        await interaction.followup.send("Roster updated!", ephemeral=True)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)

        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.update_roster(interaction, roster_channel)
            )
