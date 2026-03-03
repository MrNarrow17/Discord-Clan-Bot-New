import discord


def send_results(
    interaction: discord.Interaction, tryoutchannel: discord.TextChannel
) -> discord.Embed:

    embed = discord.Embed(
        title="🎫 Send tryout results command was used",
        description=f"{interaction.user.mention} sent tryout results to {tryoutchannel.mention}",
        color=discord.Color.blue(),
    )

    return embed
