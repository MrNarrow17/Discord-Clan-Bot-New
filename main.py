import asyncio
from threading import Thread

import discord

from bot import bot, tree, tree_groups
from commands import setup_all
from web import run_flask

tryout_result_template = discord.Embed(
    title="Tryout Results", description="", color=discord.Color.green()
)


@bot.event
async def on_ready():
    if isinstance(bot.user, discord.user.ClientUser):
        print(f"Logged in as {bot.user.name} ({bot.user.id})")
    try:
        setup_all(tree, bot)
        for group in tree_groups:
            tree.add_command(group)
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")


async def main():
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    async with bot:
        await bot.start(
            "MTQxOTQyMzkwOTU4OTE1NTk3MA.Gqw01m.8eet5Udig9j0nq7WQ1qThkDv7IaFozzHCvvDqg"
        )


if __name__ == "__main__":
    asyncio.run(main())
