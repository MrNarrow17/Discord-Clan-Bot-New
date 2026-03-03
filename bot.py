import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

fetch_group = app_commands.Group(name="fetch", description="Fetch some detail")
logchannel_group = app_commands.Group(
    name="logchannel", description="Logging channel operations"
)
supportchannel_group = app_commands.Group(
    name="supportchannel", description="Support channel operations"
)
supportrole_group = app_commands.Group(
    name="supportrole", description="Supporter roles operations"
)
purge_group = app_commands.Group(name="purge", description="Purge messages")
tryout_group = app_commands.Group(name="tryout", description="Tryout results")
roster_group = app_commands.Group(name="roster", description="Roster")

tree_groups = [
    fetch_group,
    logchannel_group,
    purge_group,
    supportchannel_group,
    supportrole_group,
    tryout_group,
    roster_group,
]
