import discord
from discord import app_commands
from discord.ext import commands

from Utilities.databaseManager import GUILD_IDS, get_enabled_modules_for_guild


async def rebuild_commands_for_guild(bot: commands.Bot, guild_id: int):
    """
    Safely rebuilds commands for a specific guild without touching global commands
    or commands for other guilds.
    """
    tree: app_commands.CommandTree = bot.tree
    guild_obj = discord.Object(id=guild_id)

    # STEP 1 — Get which modules are enabled for this guild
    enabled_modules = await get_enabled_modules_for_guild(guild_id)

    # STEP 2 — Build a list of commands that SHOULD be in this guild
    commands_for_guild = []

    for command in tree.walk_commands():
        callback = getattr(command, "callback", None)
        if callback is None:
            continue

        is_guild_bound = getattr(callback, "__guild_bound__", False)
        module_name = getattr(callback, "__module_name__", None)

        # Skip global commands
        if not is_guild_bound:
            continue

        # Skip commands whose module is disabled
        if module_name and module_name not in enabled_modules:
            continue

        commands_for_guild.append(command)

    # STEP 3 — Clear ONLY this guild's command bindings
    # This does NOT affect global commands or other guilds.
    tree.clear_commands(guild=guild_obj)

    # STEP 4 — Re-add only the commands that belong in this guild
    for cmd in commands_for_guild:
        tree.add_command(cmd, guild=guild_obj)

    print(f"Rebuilt commands for guild {guild_id}: {len(commands_for_guild)} commands.", command.name)

    print(
        command.name,
        getattr(callback, "__guild_bound__", None),
        getattr(callback, "__module_name__", None)
    )



async def sync_guild(bot: commands.Bot, guild_id: int):
    """
    Rebuild + sync commands for a single guild.
    """
    await rebuild_commands_for_guild(bot, guild_id)
    guild_obj = discord.Object(id=guild_id)
    synced = await bot.tree.sync(guild=guild_obj)
    return synced


async def sync_all_registered_guilds(bot: commands.Bot):
    """
    Master sync: rebuild + sync for all guilds in GUILD_IDS.
    """
    total = 0
    for gid in GUILD_IDS:
        synced = await sync_guild(bot, gid)
        total += len(synced)
    return total