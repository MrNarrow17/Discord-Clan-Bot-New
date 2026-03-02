import discord
from discord import app_commands

from bot import tryout_group
from settings import settings
from tools import embed_templates
from tools.logembeds import tryout_results as logging


def setup(tree, bot):
    @tryout_group.command(name="sendresults", description="Send tryout results")
    @app_commands.describe(
        member="Select the member",
        evaluator="Select the evaluator",
        movement="Rate member's movement from 0 to 10",
        aim="Rate member's aim from 0 to 10",
        gamesense="Rate member's gamesense from 0 to 10",
        final_decision="Passed or failed",
        note="Note on player",
    )
    async def send_results(
        interaction: discord.Interaction,
        member: discord.Member,
        evaluator: discord.Member,
        movement: int,
        aim: int,
        gamesense: int,
        final_decision: str,
        note: str = "",
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        tryoutchannel_id = settings.read_settings(guild, "tryoutchannel")
        if tryoutchannel_id is None:
            await interaction.followup.send(
                "Please set the tryout channel first!", ephemeral=True
            )
            return
        tryoutchannel = guild.get_channel(tryoutchannel_id)
        if not isinstance(tryoutchannel, discord.TextChannel):
            await interaction.followup.send(
                "Tryout channel is not valid!", ephemeral=True
            )
            return
        embed = embed_templates.tryout_results_template(
            member,
            evaluator,
            movement,
            aim,
            gamesense,
            final_decision,
            note,
        )
        await tryoutchannel.send(member.mention, embed=embed)
        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.send_results(interaction, tryoutchannel)
            )
        await interaction.followup.send(
            f"Sent tryout resuls to {tryoutchannel.mention}!",
            ephemeral=True,
        )
