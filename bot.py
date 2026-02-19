"""
----------------------------------------------------------------------------
This file is the main entry point for the bot. It initializes the bot, loads all cogs, and starts the bot.
----------------------------------------------------------------------------
"""


import discord
from discord.ext import commands

import os

import Utilities.botConfig as botConfig
from Utilities.databaseManager import init_db, GUILD_IDS, init_module_db
from Cogs.Modules.Core.defaultModules import enable_defaults_for_existing_guilds

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=botConfig.intents,
            application_id=botConfig.APPLICATION_ID
        )

    async def setup_hook(self):
        await init_db()
        await init_module_db()
        await enable_defaults_for_existing_guilds(self)

        await self.load_all_cogs("./Cogs")

    async def load_all_cogs(self, directory):
        base = directory.replace("\\", "/")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file).replace("\\", "/")

                    relative = full_path[len(base):].lstrip("/")

                    module = f"Cogs.{relative[:-3].replace('/', '.')}"

                    await self.load_extension(module)
                    print(f"Loaded cog: {module}")

    async def on_ready(self):
        print(
            '------------------------------------------------------------------------\n'
            f'Logged in as {self.user} (ID: {self.user.id})\n'
            '------------------------------------------------------------------------'
        )

bot = MyClient()

bot.run(botConfig.BOT_TOKEN)