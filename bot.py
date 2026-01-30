# importing necessary libraries
import discord
from discord.ext import commands

import os

# importing utilities for bot configuration and database management
import Utilities.botConfig as botConfig
from Utilities.databaseManager import init_db, GUILD_IDS

# defining the main bot client class
class MyClient(commands.Bot):
    def __init__(self):
        # initializing the bot with command prefix, intents, and application ID
        super().__init__(
            command_prefix="!",
            intents=botConfig.intents,
            application_id=botConfig.APPLICATION_ID
        )

    # setting up the bot hook to initialize the database and load cogs
    async def setup_hook(self):
        # Initialize the database
        await init_db()
        # Load all cogs recursively
        await self.load_all_cogs("./Cogs")

    # method to load all cogs from a specified directory
    async def load_all_cogs(self, directory):
        base = directory.replace("\\", "/")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file).replace("\\", "/")

                    # Remove the base directory prefix
                    relative = full_path[len(base):].lstrip("/")

                    # Convert to module path
                    module = f"Cogs.{relative[:-3].replace('/', '.')}"

                    await self.load_extension(module)
                    print(f"Loaded cog: {module}")

    # event handler for when the bot is ready
    async def on_ready(self):
        print(
            '------------------------------------------------------------------------\n'
            f'Logged in as {self.user} (ID: {self.user.id})\n'
            '------------------------------------------------------------------------'
        )

# creating an instance of the bot and running it
bot = MyClient()

# running the bot with the specified token
bot.run(botConfig.BOT_TOKEN)