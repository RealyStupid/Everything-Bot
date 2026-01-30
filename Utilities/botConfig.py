import discord
import os
from dotenv import load_dotenv #type: ignore

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

APPLICATION_ID = 1466089057103904838