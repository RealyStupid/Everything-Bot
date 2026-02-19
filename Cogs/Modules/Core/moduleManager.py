import discord
from discord.ext import commands
from discord import app_commands

from Utilities.decorators import guilds_for, module
from Utilities.databaseManager import (
    set_module_enabled,
    get_enabled_modules_for_guild,
)
from Utilities.guildBinder import sync_guild
from Utilities.customGroup import create_group
from Cogs.Modules.Core.defaultModules import DEFAULT_MODULES
from Utilities.moduleEnum import ModuleEnum


class ModuleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Create custom group (not auto-registered)
        self.module_group = create_group(
            name="module",
            description="Manage bot modules"
        )

        # Add subcommands
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
    # AUTOCOMPLETE HELPERS
    # -------------------------------------------------

    async def autocomplete_all_modules(
        self,
        interaction: discord.Interaction,
        current: str
    ):
        """Autocomplete for /module enable"""
        return [
            app_commands.Choice(name=m.value, value=m.value)
            for m in ModuleEnum
            if current.lower() in m.value.lower()
        ]

    async def autocomplete_disable_modules(
        self,
        interaction: discord.Interaction,
        current: str
    ):
        """Autocomplete for /module disable (excludes default modules)"""
        return [
            app_commands.Choice(name=m.value, value=m.value)
            for m in ModuleEnum
            if m.value not in DEFAULT_MODULES
            and current.lower() in m.value.lower()
        ]

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
            f"Enabled modules:```{text}```",
            ephemeral=True,
        )

    # -------------------------------------------------
    # /module enable
    # -------------------------------------------------
    @module("core")
    @guilds_for()
    @app_commands.describe(name="The module to enable.")
    @app_commands.autocomplete(name=autocomplete_all_modules)
    async def enable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in ModuleEnum.list():
            await interaction.response.send_message(
                f"Unknown module: `{name}`",
                ephemeral=True,
            )
            return

        await set_module_enabled(guild_id, name, True)

        await interaction.response.send_message(
            f"Enabled module `{name}` and synced commands.",
            ephemeral=True,
        )
        await sync_guild(self.bot, guild_id)

    # -------------------------------------------------
    # /module disable
    # -------------------------------------------------
    @module("core")
    @guilds_for()
    @app_commands.describe(name="The module to disable.")
    @app_commands.autocomplete(name=autocomplete_disable_modules)
    async def disable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in ModuleEnum.list():
            await interaction.response.send_message(
                f"Unknown module: `{name}`",
                ephemeral=True,
            )
            return

        if name in DEFAULT_MODULES:
            await interaction.response.send_message(
                f"❌ The `{name}` module is required and cannot be disabled.",
                ephemeral=True,
            )
            return

        await set_module_enabled(guild_id, name, False)

        await interaction.response.send_message(
            f"Disabled module `{name}` and synced commands.",
            ephemeral=True,
        )
        await sync_guild(self.bot, guild_id)


async def setup(bot: commands.Bot):
    await bot.add_cog(ModuleCog(bot))