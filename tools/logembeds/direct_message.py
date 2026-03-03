import discord


def dm(
    interaction: discord.Interaction, user: discord.User, message: str
) -> discord.Embed:

    embed = discord.Embed(
        title="📧 DM command was used",
        description=f"{interaction.user.mention} sent a direct message to {user.mention}",
        color=discord.Color.blue(),
    )

    embed.add_field(name="Content:", value=message)

    return embed
