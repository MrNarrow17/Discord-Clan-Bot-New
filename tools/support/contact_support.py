import discord

from settings import settings


class ContactSupport:
    def __init__(self):
        pass

    async def send_message_to_support(
        self, interaction: discord.Interaction, user: discord.abc.User, guild_id: int
    ) -> str:

        guild = interaction.client.get_guild(guild_id)
        if not guild:
            return "The bot can't find the guild! Try again later."

        roles = settings.read_settings(guild, "supportrole") or []
        supportchannel_id = settings.read_settings(guild, "supportchannel")

        if not supportchannel_id:
            return "Support channel is not configured by the server, can't contact support."

        supportchannel = guild.get_channel(supportchannel_id)
        if not isinstance(supportchannel, discord.TextChannel):
            return "Support channel is invalid, can't contact support."

        role_mentions = [
            role.mention
            for role_id in roles
            if (role := guild.get_role(role_id)) is not None
        ]

        message = (
            f"{'\n'.join(role_mentions)}\nPlease contact {user.mention} for assistance."
            if role_mentions
            else f"No valid support roles found.\nPlease contact {user.mention}."
        )

        await supportchannel.send(
            message, allowed_mentions=discord.AllowedMentions(roles=True, users=True)
        )

        return "Success! Soon we will contact you for help."
