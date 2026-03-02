import discord

from tools.support.contact_support import ContactSupport


class ContactSupportView(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.support_service = ContactSupport()

    @discord.ui.button(
        label="Contact Support", style=discord.ButtonStyle.primary, emoji="📩"
    )
    async def contact_support_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:

        button.disabled = True

        await interaction.response.edit_message(view=self)

        result = await self.support_service.send_message_to_support(
            interaction, interaction.user, self.guild_id
        )

        await interaction.followup.send(result, ephemeral=True)
