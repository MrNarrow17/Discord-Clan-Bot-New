import discord
from discord import app_commands

from settings import settings
from tools.logembeds import general as logging


def setup(tree, bot):
    @tree.command(name="say", description="Say something")
    @app_commands.describe(text="What to say")
    async def say(interaction: discord.Interaction, text: str):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        if isinstance(interaction.channel, discord.TextChannel):
            await interaction.channel.send(text)
            await interaction.followup.send(f"Said: {text}!", ephemeral=True)
            logchannel_id = settings.read_settings(guild, "logchannel")
            logchannel = guild.get_channel(logchannel_id)
            if isinstance(logchannel, discord.TextChannel):
                await logchannel.send(embed=logging.say(interaction))

    @tree.command(name="embed", description="Send customizable embed")
    @app_commands.describe(
        title="Title of the embed", description="Description of the embed"
    )
    async def embed(interaction: discord.Interaction, title: str, description: str):
        await interaction.response.defer(ephemeral=True)
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.followup.send("Invalid channel!", ephemeral=True)
            return
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue(),
        )
        await interaction.channel.send(embed=embed)
        await interaction.followup.send("Sent embed!", ephemeral=True)
        if interaction.guild:
            logchannel_id = settings.read_settings(interaction.guild, "logchannel")
            logchannel = interaction.guild.get_channel(logchannel_id)
            if isinstance(logchannel, discord.TextChannel):
                await logchannel.send(embed=logging.embed(interaction))

    @tree.command(name="ping", description="Ping the bot")
    async def ping(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.send_message(
            f"Pong! Bot responded in {round(bot.latency * 1000)}ms", ephemeral=True
        )
        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.ping(interaction, round(bot.latency * 1000))
            )
