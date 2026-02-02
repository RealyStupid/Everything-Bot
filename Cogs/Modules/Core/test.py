import discord
from discord.ext import commands
from discord import app_commands

from Utilities.decorators import guilds_for, module
from Utilities.databaseManager import GUILD_IDS

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    @module("core")
    @guilds_for()
    #@app_commands.guilds(*[discord.Object(id=g) for g in GUILD_IDS])
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await interaction.response.send_message(f"Pong! Latency: {latency:.2f} ms")

async def setup(bot):
    await bot.add_cog(TestCog(bot))