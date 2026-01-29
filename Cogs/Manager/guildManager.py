import discord
from discord.ext import commands
from Utilities import databaseManager as guildDB


class guildManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addguild")
    @commands.is_owner()
    async def add_guild(self, ctx, guild_id: int):
        added = await guildDB.register_guild(guild_id)
        if added:
            await ctx.send(f"Guild `{guild_id}` added.")
        else:
            await ctx.send("Guild already exists.")

    @commands.command(name="removeguild")
    @commands.is_owner()
    async def remove_guild(self, ctx, guild_id: int):
        removed = await guildDB.unregister_guild(guild_id)
        if removed:
            await ctx.send(f"Guild `{guild_id}` removed.")
        else:
            await ctx.send("Guild not found.")

    @commands.command(name="listguilds")
    @commands.is_owner()
    async def list_guilds(self, ctx):
        guilds = await guildDB.get_registered_guilds()
        if not guilds:
            await ctx.send("No guilds registered.")
        else:
            formatted = "\n".join(str(g) for g in guilds)
            await ctx.send(f"Registered guilds:\n```\n{formatted}\n```")


async def setup(bot):
    await bot.add_cog(guildManager(bot))
