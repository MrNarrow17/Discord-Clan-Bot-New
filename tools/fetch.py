import discord


class Fetch:
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    async def fetch_roles(
        self, interaction: discord.Interaction
    ) -> list[discord.Role] | None:
        if isinstance(interaction.guild, discord.Guild):
            return list(interaction.guild.roles[::-1])

        else:
            return None

    async def fetch_messages(
        self, channel: discord.TextChannel, amount: int
    ) -> list[discord.Message]:
        messages = []
        async for message in channel.history(limit=amount):
            messages.append(message)

        return messages

    async def fetch_members_with_role(
        self, guild: discord.Guild, role_id: int
    ) -> list[discord.Member]:

        role = guild.get_role(role_id)

        if role is None:
            return []

        return role.members
