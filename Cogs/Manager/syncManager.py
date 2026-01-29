import discord
from discord.ext import commands

from Utilities.databaseManager import GUILD_IDS
class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sync', help='Syncs the application commands with Discord.')
    @commands.is_owner()
    async def sync(self, ctx):
        total = 0

        for guild_id in GUILD_IDS:
            guild = discord.Object(id=guild_id)
            try:
                synced = await self.bot.tree.sync(guild=guild)
                total += len(synced)
                print(f"synced {synced} commands to {guild_id}")
            except Exception as e:
                await print(f"an error acured: {e}")

        await ctx.send(f"Synced commands to {len(GUILD_IDS)} guilds ({total} commands total).")

async def setup(bot):
    await bot.add_cog(SyncCog(bot))