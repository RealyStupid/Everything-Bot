import discord
from discord.ext import commands
from discord import app_commands

from Utilities.databaseManager import GUILD_IDS

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getguild(guild_id_list: vars):
        guilds = []
        for guild_id in guild_id_list:
            guild = discord.Object(id=guild_id)
            guilds.append(guild)
        return guilds

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await interaction.response.send_message(f"Pong! Latency: {latency:.2f} ms")

async def setup(bot):
    await bot.add_cog(TestCog(bot))
    for gid in GUILD_IDS:
        bot.tree.copy_global_to(guild=discord.Object(id=gid))
        await bot.tree.sync(guild=discord.Object(id=gid))