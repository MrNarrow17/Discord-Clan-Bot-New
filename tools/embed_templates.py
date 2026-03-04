import discord


def tryout_results_template(
    member: discord.Member,
    evaluator: discord.Member,
    movement: float,
    aim: float,
    gamesense: float,
    final_decision: str,
    note: str,
) -> discord.Embed:

    passed = final_decision == "Passed"
    color = 0x57F287 if passed else 0xED4245
    average = round((movement + aim + gamesense) / 3, 1)

    embed = discord.Embed(
        title="⚔️ Tryout Results",
        description=(
            f"```\n  Average Score: {average}/10  ·  Decision: {final_decision}\n```"
        ),
        color=color,
        timestamp=discord.utils.utcnow(),
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    participant_text = (
        f"> `👤` {member.mention} ─ **Tryouted Member**\n"
        f"> `🛡` {evaluator.mention} ─ **Evaluator**"
    )

    embed.add_field(
        name="▸ 📋 Participants",
        value=f"{participant_text}\n\u200b",
        inline=False,
    )

    scores_text = (
        f"> `🏃` **Movement** ─ **{movement}**/10\n"
        f"> `🎯` **Aim** ─ **{aim}**/10\n"
        f"> `🧠` **Game Sense** ─ **{gamesense}**/10"
    )

    embed.add_field(
        name="▸ 📊 Scores",
        value=f"{scores_text}\n\u200b",
        inline=False,
    )

    embed.add_field(
        name="▸ 📝 Note",
        value=f"> {note}\n\u200b" if note else "> *No additional notes.*\n\u200b",
        inline=False,
    )

    embed.set_footer(
        text=f"🏠 {member.guild.name} • Tryout evaluated",
        icon_url=member.guild.icon.url if member.guild.icon else None,
    )

    return embed


def roster_embed(
    guild: discord.Guild,
    members: list[discord.Member],
    sub_members: list[discord.Member],
) -> discord.Embed:

    total = len(members) + len(sub_members)

    embed = discord.Embed(
        title=f"⚔️ {guild.name} — Clan Roster",
        description=(
            f"```\n"
            f"  Total: {total} players  ·  {len(members)} main  ·  {len(sub_members)} subs\n"
            f"```"
        ),
        color=0x5865F2,
        timestamp=discord.utils.utcnow(),
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    if members:
        member_text = "\n".join(
            f"> `{i:>2}.` {m.mention}" for i, m in enumerate(members, start=1)
        )
    else:
        member_text = "> *No members registered.*"

    embed.add_field(
        name="▸ 👥 Members",
        value=f"{member_text}\n\u200b",
        inline=False,
    )

    if sub_members:
        sub_member_text = "\n".join(
            f"> `{i:>2}.` {m.mention}" for i, m in enumerate(sub_members, start=1)
        )
    else:
        sub_member_text = "> *No subs registered.*"

    embed.add_field(
        name="▸ ⚔️ Substitutes",
        value=f"{sub_member_text}\n\u200b",
        inline=False,
    )

    embed.set_footer(
        text=f"🏠 {guild.name} • Roster last updated",
        icon_url=guild.icon.url if guild.icon else None,
    )

    return embed
