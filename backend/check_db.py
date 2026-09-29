# check_db.py
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def main():
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        )
        tables = [row[0] for row in result]
        print("Tables in DB:", tables)

        # Also show the alembic version
        try:
            ver = await conn.execute(text("SELECT version_num FROM alembic_version"))
            print("Alembic version:", [row[0] for row in ver])
        except Exception as e:
            print("No alembic_version table:", e)


if __name__ == "__main__":
    asyncio.run(main())