import discord


def add_support_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⛑️ Support role was added",
        description=f"{interaction.user.mention} added {role.mention} as a support role",
        color=discord.Color.blue(),
    )

    return embed


def remove_support_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⛑️ Support role was removed",
        description=f"{interaction.user.mention} removed {role.mention} from list of support roles",
        color=discord.Color.blue(),
    )

    return embed


def list_support_role(interaction: discord.Interaction) -> discord.Embed:

    embed = discord.Embed(
        title="⛑️ Support roles were listed",
        description=f"{interaction.user.mention} listed support roles",
        color=discord.Color.blue(),
    )

    return embed


def set_clan_member_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Clan member role was set",
        description=f"{interaction.user.mention} set {role.mention} as clan member role",
        color=discord.Color.blue(),
    )

    return embed


def remove_clan_member_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Clan member role was set",
        description=f"{interaction.user.mention} removed {role.mention} as clan member role",
        color=discord.Color.blue(),
    )

    return embed


def set_sub_clan_member_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Sub clan member role was set",
        description=f"{interaction.user.mention} set {role.mention} as sub clan member role",
        color=discord.Color.blue(),
    )

    return embed


def remove_sub_clan_member_role(
    interaction: discord.Interaction, role: discord.Role
) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Sub clan member role was set",
        description=f"{interaction.user.mention} removed {role.mention} as sub clan member role",
        color=discord.Color.blue(),
    )

    return embed
