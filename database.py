import aiosqlite

async def setup_db():
    async with aiosqlite.connect("frakcje.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            faction TEXT,
            xp INTEGER,
            level INTEGER
        )""")
        await db.commit()
    await setup_missions_table()


async def add_xp(user_id, faction, xp_amount):
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT xp, level FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            xp, level = row
            xp += xp_amount
            # Level up co 100 XP
            new_level = xp // 100 + 1
            await db.execute("UPDATE users SET xp = ?, level = ? WHERE user_id = ?", (xp, new_level, user_id))
        else:
            await db.execute("INSERT INTO users (user_id, faction, xp, level) VALUES (?, ?, ?, ?)", (user_id, faction, xp_amount, 1))
        await db.commit()

async def get_user_data(user_id):
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT faction, xp, level FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()

async def setup_faction_table():
    async with aiosqlite.connect("frakcje.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS faction_points (
                faction TEXT PRIMARY KEY,
                points INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def add_faction_points(faction_name, points):
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT points FROM factions WHERE name = ?", (faction_name,))
        row = await cursor.fetchone()
        if row:
            current = row[0]
            await db.execute("UPDATE factions SET points = ? WHERE name = ?", (current + points, faction_name))
        else:
            await db.execute("INSERT INTO factions (name, points) VALUES (?, ?)", (faction_name, points))
        await db.commit()

async def get_faction_points():
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT name, points FROM factions ORDER BY points DESC")
        return await cursor.fetchall()
async def setup_missions_table():
    async with aiosqlite.connect("frakcje.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                user_id INTEGER PRIMARY KEY,
                last_completed TEXT
            )
        """)
        await db.commit()
async def get_all_user_data():
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT faction, xp, level FROM users")
        return await cursor.fetchall()

async def get_faction_points():
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT faction, points FROM faction_points")
        return await cursor.fetchall()
