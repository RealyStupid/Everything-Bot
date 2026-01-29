import aiosqlite

DB_PATH = "Data/bot_database.db"
GUILD_IDS = []

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

async def refresh_cache():
    """Reloads the global GUILD_IDS list from the database."""
    global GUILD_IDS
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT guild_id FROM guilds")
        rows = await cursor.fetchall()
        GUILD_IDS = [row[0] for row in rows]

async def register_guild(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("INSERT INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.commit()
            await refresh_cache()
            return True
        except aiosqlite.IntegrityError:
            return False

async def unregister_guild(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("DELETE FROM guilds WHERE guild_id = ?", (guild_id,))
        await db.commit()
        await refresh_cache()
        return cursor.rowcount > 0

async def get_registered_guilds():
    return GUILD_IDS