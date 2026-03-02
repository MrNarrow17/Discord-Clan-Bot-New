import discord
from discord import app_commands

from bot import logchannel_group, roster_group, supportchannel_group, tryout_group
from settings import settings
from tools.logembeds import channels as logging


def setup(tree, bot):

    @logchannel_group.command(name="set", description="Set the logging channel")
    @app_commands.describe(channel="Select the logging channel")
    async def set_logging_channel(
        interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        await channel.send(embed=logging.logchannel_set(interaction, channel))
        settings.write_settings(guild, "logchannel", channel.id)
        await interaction.followup.send("Success!", ephemeral=True)

    @logchannel_group.command(name="remove", description="Remove the logging channel")
    @app_commands.describe()
    async def remove_logging_channel(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "logchannel", None)
        await interaction.followup.send("Success!", ephemeral=True)

    @supportchannel_group.command(name="set", description="Set the support channel")
    @app_commands.describe(channel="Select the support channel")
    async def set_support_channel(
        interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "supportchannel", channel.id)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.supportchannel_set(interaction, channel)
            )
        await interaction.followup.send("Success!", ephemeral=True)

    @supportchannel_group.command(
        name="remove", description="Remove the support channel"
    )
    @app_commands.describe()
    async def remove_support_channel(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "supportchannel", None)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.supportchannel_remove(interaction))
        await interaction.followup.send("Success!", ephemeral=True)

    @tryout_group.command(
        name="setchannel", description="Set channel of tryout results"
    )
    @app_commands.describe(channel="Select the tryout results channel")
    async def tryout_setchannel(
        interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "tryoutchannel", channel.id)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.tryoutchannel_set(interaction, channel))
        await interaction.followup.send("Success!", ephemeral=True)

    @tryout_group.command(name="removechannel", description="Remove the tryout channel")
    @app_commands.describe()
    async def remove_tryout_channel(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "tryoutchannel", None)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.tryoutchannel_remove(interaction))
        await interaction.followup.send("Success!", ephemeral=True)

    @roster_group.command(name="setchannel", description="Set channel of roster")
    @app_commands.describe(channel="Select the roster channel")
    async def set_roster_channel(
        interaction: discord.Interaction, channel: discord.TextChannel
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "rosterchannel", channel.id)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.rosterchannel_set(interaction, channel))
            await interaction.followup.send("Success!", ephemeral=True)

    @roster_group.command(name="removechannel", description="Remove the roster channel")
    @app_commands.describe()
    async def remove_roster_channel(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "rosterchannel", None)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.rosterchannel_remove(interaction))
        await interaction.followup.send("Success!", ephemeral=True)
