import discord
from discord.ext import commands

import os
import Utilities.botConfig as botConfig
from Utilities.databaseManager import init_db, GUILD_IDS

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=botConfig.intents,
            application_id=botConfig.APPLICATION_ID
        )

    async def setup_hook(self):
        # Initialize the database
        await init_db()
        # Load all cogs recursively
        await self.load_all_cogs("./Cogs")

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

    async def on_ready(self):
        print(
            '------------------------------------------------------------------------\n'
            f'Logged in as {self.user} (ID: {self.user.id})\n'
            '------------------------------------------------------------------------'
        )

bot = MyClient()

bot.run(botConfig.BOT_TOKEN)