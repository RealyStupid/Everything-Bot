import discord
from discord.ext import commands

from Utilities.guildBinder import sync_guild
from Utilities.databaseManager import GUILD_IDS


class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx):
        await ctx.send("Syncing all guilds...")

        total = 0
        for guild_id in GUILD_IDS:
            synced = await sync_guild(self.bot, guild_id)
            total += len(synced)

        await ctx.send(f"Synced {total} commands across {len(GUILD_IDS)} guilds.")


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
