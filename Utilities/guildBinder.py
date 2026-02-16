import discord
from discord import app_commands
from discord.ext import commands

from Utilities.databaseManager import ( # type: ignore
    GUILD_IDS,
    get_enabled_modules_for_guild,
)
from Utilities.customGroup import REGISTERED_GROUPS # type: ignore


async def rebuild_commands_for_guild(bot: commands.Bot, guild_id: int):
    """
    Safely rebuilds commands for a specific guild.

    It handles two sources of commands:

      1) "Normal" app commands that discord.py already knows about
         (e.g., /ping), discovered via tree.walk_commands().

      2) Custom groups and their subcommands that we registered in
         Utilities.custom_groups.REGISTERED_GROUPS, which are NOT
         auto-registered and only get added here.
    """
    tree: app_commands.CommandTree = bot.tree
    guild_obj = discord.Object(id=guild_id)

    enabled_modules = await get_enabled_modules_for_guild(guild_id)

    commands_for_guild: list[app_commands.Command | app_commands.Group] = []

    # -------------------------------------------------
    # 1) Handle "normal" commands (like /ping)
    # -------------------------------------------------
    for command in tree.walk_commands():
        # Skip groups here; we only want leaf commands from this source.
        if isinstance(command, app_commands.Group):
            continue

        callback = getattr(command, "callback", None)
        if callback is None:
            continue

        is_guild_bound = getattr(callback, "__guild_bound__", False)
        module_name = getattr(callback, "__module_name__", None)

        if not is_guild_bound:
            continue

        if module_name and module_name not in enabled_modules:
            continue

        commands_for_guild.append(command)

    # -------------------------------------------------
    # 2) Handle custom groups from our registry
    # -------------------------------------------------
    for group in REGISTERED_GROUPS:
        # decides per subcommand whether this group should exist
        # in this guild. If at least one subcommand is allowed, add
        # the group and its allowed subcommands.
        allowed_subcommands: list[app_commands.Command] = []

        for sub in group.commands:
            callback = getattr(sub, "callback", None)
            if callback is None:
                continue

            is_guild_bound = getattr(callback, "__guild_bound__", False)
            module_name = getattr(callback, "__module_name__", None)

            if not is_guild_bound:
                continue

            if module_name and module_name not in enabled_modules:
                continue

            allowed_subcommands.append(sub)

        if not allowed_subcommands:
            # No subcommands of this group are allowed in this guild.
            continue

        # We want the group itself to be present in this guild.
        # When we add the group to the tree, its subcommands come along.
        commands_for_guild.append(group)

    # -------------------------------------------------
    # 3) Clear ONLY this guild's commands
    # -------------------------------------------------
    tree.clear_commands(guild=guild_obj)

    # -------------------------------------------------
    # 4) Re-add only the commands that belong in this guild
    # -------------------------------------------------
    for cmd in commands_for_guild:
        tree.add_command(cmd, guild=guild_obj)

    names = [cmd.qualified_name for cmd in commands_for_guild]
    print(f"[SYNC] Rebuilt commands for guild {guild_id}: {len(commands_for_guild)} commands -> {names}")


async def sync_guild(bot: commands.Bot, guild_id: int):
    await rebuild_commands_for_guild(bot, guild_id)
    guild_obj = discord.Object(id=guild_id)
    synced = await bot.tree.sync(guild=guild_obj)
    print(f"[SYNC] Synced guild {guild_id}: {len(synced)} commands.")
    return synced


async def sync_all_registered_guilds(bot: commands.Bot):
    total = 0
    for gid in GUILD_IDS:
        synced = await sync_guild(bot, gid)
        total += len(synced)

    print(f"[SYNC] Finished syncing all registered guilds. Total commands synced: {total}")
    return total
