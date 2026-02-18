# Import necessary libraries
import discord
import os
from dotenv import load_dotenv #type: ignore

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True

# Load bot token from environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Define application ID
APPLICATION_ID = 1473666490388578314