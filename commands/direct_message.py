import discord
from discord import app_commands

from settings import settings
from tools.logembeds import direct_message as logging
from tools.ui import ContactSupportView


def setup(tree, bot):

    @tree.command(name="dm", description="Send a direct message to someone")
    @app_commands.describe(
        user="User to send the message to",
        text="What to say",
        anonymous="Do you want to send the message anonymously?",
    )
    async def dm(
        interaction: discord.Interaction,
        user: discord.User,
        text: str,
        anonymous: bool = True,
    ):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Invalid guild!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        if user.bot:
            await interaction.followup.send("You can't warn a bot!", ephemeral=True)
        else:
            try:
                server_name = f"**{guild}**" if guild else "unknown server"

                embed = discord.Embed(
                    title="⚔️ Staff Message",
                    description=(
                        f"```\n  Server: {guild or 'Unknown Server'}  ·  Type: Direct Message\n```"
                    ),
                    color=0x5865F2,
                    timestamp=discord.utils.utcnow(),
                )

                embed.add_field(
                    name="▸ 📋 Sender",
                    value=(
                        "> `🛡` **From** ─ "
                        + (
                            f"{interaction.user.mention} ─ Staff of **{server_name}**"
                            if not anonymous
                            else f"Staff of **{server_name}**"
                        )
                    )
                    + "\n\u200b",
                    inline=False,
                )

                embed.add_field(
                    name="▸ 📧 Message",
                    value=f"> {text}\n\u200b",
                    inline=False,
                )

                embed.set_footer(
                    text=f"🏠 {server_name} • Staff message",
                )

                supportrole = settings.read_settings(guild, "supportrole")

                if supportrole:
                    view = ContactSupportView(guild.id)
                    await user.send(embed=embed, view=view)
                else:
                    await user.send(embed=embed)

                await interaction.followup.send(
                    f"DM sent to {user.mention}!", ephemeral=True
                )

                logchannel_id = settings.read_settings(guild, "logchannel")
                logchannel = guild.get_channel(logchannel_id)
                if isinstance(logchannel, discord.TextChannel):
                    await logchannel.send(embed=logging.dm(interaction, user, text))

            except discord.Forbidden:
                await interaction.followup.send(
                    "Could not send DM. The user might have DMs disabled.",
                    ephemeral=True,
                )
            except Exception as e:
                await interaction.followup.send(
                    f"An error occurred: {e}",
                    ephemeral=True,
                )
