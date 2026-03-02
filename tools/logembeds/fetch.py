import discord


def fetch_roles(interaction: discord.Interaction) -> discord.Embed:

    embed = discord.Embed(
        title="🎫 Fetch roles command was used",
        description=f"{interaction.user.mention} fetched roles",
        color=discord.Color.blue(),
    )

    return embed
