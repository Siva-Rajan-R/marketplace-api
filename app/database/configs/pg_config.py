from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from icecream import ic
import os
load_dotenv()

PG_DATABASE_URL = os.getenv("PG_DATABASE_URL")

ENGINE=create_async_engine(PG_DATABASE_URL,echo=False)

BASE=declarative_base()


AsyncLocalSession=async_sessionmaker(ENGINE)

async def init_pg_db():
    try:
        ic("initializing pg db...")
        async with ENGINE.connect() as conn:
            await conn.run_sync(BASE.metadata.create_all)
    except Exception as e:
        ic(f"Error : initializing pg db => {e}")


async def get_pg_async_session():
    Session=AsyncLocalSession()
    try:
        yield Session
    finally:
        await Session.close()