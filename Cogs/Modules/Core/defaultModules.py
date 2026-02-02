import discord
from discord.ext import commands

from Utilities.databaseManager import set_module_enabled
from Utilities.guildBinder import sync_guild


DEFAULT_MODULES = ["core", "manager"]  # modules enabled for every new guild

async def enable_defaults_for_existing_guilds(bot):
    for guild in bot.guilds:
        for module in DEFAULT_MODULES:
            await set_module_enabled(guild.id, module, True)

        await sync_guild(bot, guild.id)

class GuildEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        # Enable default modules
        for module in DEFAULT_MODULES:
            await set_module_enabled(guild.id, module, True)

        # Sync commands for this guild
        await sync_guild(self.bot, guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        # Optional: clean up DB entries
        pass


async def setup(bot):
    await bot.add_cog(GuildEvents(bot))