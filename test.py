import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect("postgresql://admin:root@postgres:5432/test_db")
    rows = await conn.fetch("SELECT 1")
    print(rows)
    await conn.close()

asyncio.run(test())