import discord
from discord.ext import commands
from discord import app_commands

from Utilities.decorators import guilds_for, module
from Utilities.databaseManager import set_module_enabled, get_enabled_modules_for_guild, GUILD_IDS
from Utilities.guildBinder import sync_guild

# Define what modules exist in your system
AVAILABLE_MODULES = ["core", "moderation", "fun", "logging"]

class ModuleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    module_group = app_commands.Group(name="module", description="Manage bot modules")

    @module_group.command(name="list", description="List enabled modules for this guild")
    @module("core")
    @guilds_for()
    async def list_modules(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        enabled = await get_enabled_modules_for_guild(guild_id)
        text = ", ".join(enabled) if enabled else "No modules enabled."
        await interaction.response.send_message(f"Enabled modules: {text}", ephemeral=True)

    @module_group.command(name="enable", description="Enable a module for this guild")
    @module("core")
    @guilds_for()
    async def enable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in AVAILABLE_MODULES:
            await interaction.response.send_message(f"Unknown module: `{name}`", ephemeral=True)
            return

        await set_module_enabled(guild_id, name, True)
        await sync_guild(self.bot, guild_id)
        await interaction.response.send_message(f"Enabled module `{name}` and synced commands.", ephemeral=True)

    @module_group.command(name="disable", description="Disable a module for this guild")
    @module("core")
    @guilds_for()
    async def disable_module(self, interaction: discord.Interaction, name: str):
        guild_id = interaction.guild_id

        if name not in AVAILABLE_MODULES:
            await interaction.response.send_message(f"Unknown module: `{name}`", ephemeral=True)
            return

        await set_module_enabled(guild_id, name, False)
        await sync_guild(self.bot, guild_id)
        await interaction.response.send_message(f"Disabled module `{name}` and synced commands.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ModuleCog(bot))
