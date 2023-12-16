import asyncio

import pytest
from dotenv import load_dotenv
from sqlalchemy import DDL

# Environment must be loaded before importing any modules that depend on it
load_dotenv(".env.tests", verbose=False, override=True)  # type: ignore

from src.database import SCHEMA_NAME, engine, metadata  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.execute(
            DDL('CREATE SCHEMA IF NOT EXISTS "%(schema)s"', {"schema": SCHEMA_NAME})
        )
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    yield
