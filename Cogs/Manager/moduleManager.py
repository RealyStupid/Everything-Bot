import discord
from discord.ext import commands
from discord import app_commands

from Utilities.decorators import guilds_for, module
from Utilities.databaseManager import (
    set_module_enabled,
    get_enabled_modules_for_guild,
)
from Utilities.guildBinder import sync_guild
from Utilities.customGroup import create_group  # <-- new

AVAILABLE_MODULES = ["core", "moderation", "fun", "logging"]


class ModuleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Create a custom group that is NOT auto-registered.
        # It only lives in our registry until the sync engine uses it.
        self.module_group = create_group(
            name="module",
            description="Manage bot modules"
        )

        # Attach subcommands to the group.
        # These are real app_commands.Command objects, but again:
        # we do NOT add them to bot.tree here.
        self.module_group.add_command(
            app_commands.Command(
                name="list",
                description="List enabled modules for this guild.",
                callback=self.list_modules,
            )
        )

        self.module_group.add_command(
            app_commands.Command(
                name="enable",
                description="Enable a module for this guild.",
                callback=self.enable_module,
            )
        )

        self.module_group.add_command(
            app_commands.Command(
                name="disable",
                description="Disable a module for this guild.",
                callback=self.disable_module,
            )
        )

    # -------------------------------------------------
    # /module list
    # -------------------------------------------------
    @module("core")
    @guilds_for()
    async def list_modules(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        enabled = await get_enabled_modules_for_guild(guild_id)
        text = ", ".join(enabled) if enabled else "No modules enabled."
        await interaction.response.send_message(
            f"Enabled modules: {text}",
            ephemeral=True,
        )

    # -------------------------------------------------
    # /module enable
    # -------------------------------------------------
    @module("core")
    @guilds_for()
    @app_commands.describe(name="The module to enable.")
    async def enable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in AVAILABLE_MODULES:
            await interaction.response.send_message(
                f"Unknown module: `{name}`",
                ephemeral=True,
            )
            return

        await set_module_enabled(guild_id, name, True)
        await sync_guild(self.bot, guild_id)
        await interaction.response.send_message(
            f"Enabled module `{name}` and synced commands.",
            ephemeral=True,
        )

    # -------------------------------------------------
    # /module disable
    # -------------------------------------------------
    @module("core")
    @guilds_for()
    @app_commands.describe(name="The module to disable.")
    async def disable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in AVAILABLE_MODULES:
            await interaction.response.send_message(
                f"Unknown module: `{name}`",
                ephemeral=True,
            )
            return

        await set_module_enabled(guild_id, name, False)
        await sync_guild(self.bot, guild_id)
        await interaction.response.send_message(
            f"Disabled module `{name}` and synced commands.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ModuleCog(bot))
