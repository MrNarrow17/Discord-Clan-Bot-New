import discord
from discord import app_commands

from bot import roster_group, supportrole_group
from settings import settings
from tools.logembeds import roles as logging


def setup(tree, bot):

    @supportrole_group.command(name="add", description="Add supporter role")
    @app_commands.describe(role="Select the supporter role")
    async def add_support_role(interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        roles = settings.read_settings(guild, "supportrole") or []

        roles.append(role.id)
        print(roles)
        settings.write_settings(guild, "supportrole", roles)
        await interaction.followup.send(
            f"Added new supporter role: {role.mention}!", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.add_support_role(interaction, role))

    @supportrole_group.command(name="remove", description="Set supporter role")
    @app_commands.describe(role="Remove the supporter role")
    async def remove_support_role(interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        roles = settings.read_settings(guild, "supportrole") or []
        if role.id in roles:
            roles.remove(role.id)
            settings.write_settings(guild, "supportrole", roles)
            await interaction.followup.send(
                f"{role} role was removed from list of support roles!",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                "This role is not in the list of roles!", ephemeral=True
            )
        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.remove_support_role(interaction, role))

    @supportrole_group.command(name="list", description="List all supporter roles")
    @app_commands.describe()
    async def list_support_roles(interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        roles = settings.read_settings(guild, "supportrole") or []
        if not roles:
            await interaction.followup.send(
                "Supporter role list is empty!", ephemeral=True
            )

            return
        role_mentions = []

        for role_id in roles:
            role = guild.get_role(role_id)
            if role is not None:
                role_mentions.append(role.mention)

        embed = discord.Embed(
            title="Supporter Roles",
            description="\n".join(role_mentions) or "No valid roles found.",
            color=discord.Color.blue(),
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.list_support_role(interaction))

    @roster_group.command(name="setmemberrole", description="Set clan member role")
    @app_commands.describe(role="Select the supporter role")
    async def set_member_role(interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "memberrole", role.id)
        await interaction.followup.send(
            f"Set clan member role: {role.mention}!", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(embed=logging.set_clan_member_role(interaction, role))

    @roster_group.command(
        name="removememberrole", description="Remove clan member role"
    )
    @app_commands.describe(role="Select the supporter role")
    async def remove_member_role(interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "memberrole", None)
        await interaction.followup.send(
            f"Removed clan member role: {role.mention}!", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.remove_clan_member_role(interaction, role)
            )

    @roster_group.command(name="setsubmemberrole", description="Set clan member role")
    @app_commands.describe(role="Select the supporter role")
    async def set_sub_member_role(interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "submemberrole", role.id)
        await interaction.followup.send(
            f"Set clan sub member role: {role.mention}!", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.set_sub_clan_member_role(interaction, role)
            )

    @roster_group.command(
        name="removesubmemberrole", description="Remove clan member role"
    )
    @app_commands.describe(role="Select the supporter role")
    async def remove_sub_member_role(
        interaction: discord.Interaction, role: discord.Role
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        settings.write_settings(guild, "submemberrole", None)
        await interaction.followup.send(
            f"Removed clan sub member role: {role.mention}!", ephemeral=True
        )

        logchannel_id = settings.read_settings(guild, "logchannel")
        logchannel = guild.get_channel(logchannel_id)
        if isinstance(logchannel, discord.TextChannel):
            await logchannel.send(
                embed=logging.remove_sub_clan_member_role(interaction, role)
            )
