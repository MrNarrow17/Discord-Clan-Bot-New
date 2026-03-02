import discord

from bot import fetch_group
from settings import settings
from tools.fetch import Fetch
from tools.logembeds import fetch as logging


def setup(tree, bot):
    fetch = Fetch(bot)

    @fetch_group.command(name="roles", description="Fetch all roles")
    async def fetch_roles(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        roles = await fetch.fetch_roles(interaction)

        if not roles:
            await interaction.followup.send("Error: No roles found!", ephemeral=True)

        else:
            embed = discord.Embed(
                title="Roles",
                description="\n ".join(role.mention for role in roles),
                color=discord.Color.blue(),
            )

            await interaction.followup.send(embed=embed)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.fetch_roles(interaction))
