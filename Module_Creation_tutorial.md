# 📦 EVERYTHING BOT — Module Creation Tutorial

This guide walks you through creating a new module for EVERYTHING BOT using its modular architecture and custom command group API.

Modules in EVERYTHING BOT are:

- Fully optional  
- Per‑guild toggleable  
- Easy to create  
- Automatically synced  
- Cleanly separated from core logic  

If you want to add new features to the bot, this is the place to start.

---

## 🧩 What Is a Module?

A **module** is a logical group of commands that can be enabled or disabled per guild.

Examples:

- `core`
- `moderation`
- `fun`
- `logging`
- `economy`
- `music`

Modules are not folders or files — they are **names** used by the sync engine and decorators to control which commands appear in which guilds.

---

## 🛠️ Step 1 — Create Your Cog

Create a new file inside:
`Cogs/Modules/"your_module_name"/ .py file should be in here related to the madule`

For example, to create a "fun" module, create:
`Cogs/Modules/fun/fun_commands.py`

Inside this file, create a new Cog class:
```python
import discord
from discord.ext import commands
from discord import app_commands

from Utilities.decorators import module, guilds_for
```

Define your Cog:
```python
class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
```

Then register the Cog:
```python
async def setup(bot):
    await bot.add_cog(FunCog(bot))
```

---
## ⚙️ Step 2 — Add Commands to Your Cog

Commands are normal slash commands decorated with:
```python
@module("<module_name>")
@guilds_for()
```
Example:
```python
class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="joke", description="Tells a random joke.")
    @module("fun")
    @guilds_for()
    async def joke(self, interaction: discord.Interaction):
        await interaction.response.send_message("Why did the chicken cross the road? To get to the other side!")
```

---

## 🧩 Step 3 — (Optional) Create a Custom Group
If your module needs grouped commands like:
```
/fun joke
/fun meme
/fun roast
```

Use the custom group API:
```python
from Utilities.custom_groups import create_group

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.fun_group = create_group(
            name="fun",
            description="Fun and entertainment commands"
        )

        self.fun_group.add_command(
            app_commands.Command(
                name="joke",
                description="Tell a random joke",
                callback=self.joke
            )
        )
```
Then define the callback:
```python
@module("fun")
@guilds_for()
async def joke(self, interaction: discord.Interaction):
    await interaction.response.send_message("Here's a joke!")
```

The sync engine will:
- Only add the group if at least one subcommand is allowed
- Only add allowed subcommands
- Never auto‑register anything globally

---
## 🧩 Step 4 — Add Your Module to the Database
In Cogs/Manager/ModuleManager.py, add your module name to the list of available modules:

`AVAILABLE_MODULES = ["core", "moderation", "fun", "logging", "economy"]`

This allows:
- `/module enable fun`
- `/module disable fun`

NOTE: core is a special module that cannot be disabled.

---
## 🧩 Step 5 — Sync the Bot
Run:
`!sync`

The sync engine will:
- Rebuild commands for each guild
- Add your new module’s commands where allowed
- Remove them where disabled

You should see output like:
```
[SYNC] Rebuilt commands for guild 123: 2 commands -> ['fun joke', 'fun meme']
[SYNC] Synced guild 123: 2 commands.
```
---
