# This module manages the SQLite database for storing registered guild IDs.
# It provides functions to initialize the database, register/unregister guilds, and retrieve the list of registered guilds.
# It also maintains a global cache of guild IDs for quick access.
import aiosqlite

# Path to the SQLite database file
DB_PATH = "Data/bot_database.db"

# Global cache for guild IDs
GUILD_IDS = []

# Initialize the database and create the necessary table if it doesn't exist
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id INTEGER PRIMARY KEY
            )
        """)
        await db.commit()

    # Load initial cache
    await refresh_cache()

# Refresh the global GUILD_IDS list from the database
async def refresh_cache():
    """Reloads the global GUILD_IDS list from the database."""
    global GUILD_IDS
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT guild_id FROM guilds")
        rows = await cursor.fetchall()
        GUILD_IDS = [row[0] for row in rows]

# Register a guild by its ID
async def register_guild(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("INSERT INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.commit()
            await refresh_cache()
            return True
        except aiosqlite.IntegrityError:
            return False
        await refresh_cache()

# Unregister a guild by its ID
async def unregister_guild(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("DELETE FROM guilds WHERE guild_id = ?", (guild_id,))
        await db.commit()
        await refresh_cache()
        return cursor.rowcount > 0
    await refresh_cache()

# Retrieve the list of registered guild IDs
async def get_registered_guilds():
    return GUILD_IDS


# Module DataBase

# Initialize the module management table
# Create table to manage module states per guild
# The table contains guild_id, module_name, and enabled status
async def init_module_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS guild_modules (
                guild_id    INTEGER NOT NULL,
                module_name TEXT    NOT NULL,
                enabled     INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (guild_id, module_name)
            )
        """)
        await db.commit()

# Set the enabled state of a module for a specific guild
async def set_module_enabled(guild_id: int, module_name: str, enabled: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        if enabled:
            await db.execute("""
                INSERT INTO guild_modules (guild_id, module_name, enabled)
                VALUES (?, ?, 1)
                ON CONFLICT(guild_id, module_name) DO UPDATE SET enabled = 1
            """, (guild_id, module_name))
        else:
            await db.execute("""
                UPDATE guild_modules
                SET enabled = 0
                WHERE guild_id = ? AND module_name = ?
            """, (guild_id, module_name))
        await db.commit()

# Check if a module is enabled for a specific guild
async def is_module_enabled(guild_id: int, module_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT enabled FROM guild_modules
            WHERE guild_id = ? AND module_name = ?
        """, (guild_id, module_name))
        row = await cursor.fetchone()
        return bool(row and row[0])

# Retrieve a list of enabled modules for a specific guild
async def get_enabled_modules_for_guild(guild_id: int) -> list[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT module_name FROM guild_modules
            WHERE guild_id = ? AND enabled = 1
        """, (guild_id,))
        rows = await cursor.fetchall()
        return [r[0] for r in rows]
