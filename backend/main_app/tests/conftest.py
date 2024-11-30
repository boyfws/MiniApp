import asyncio
from typing import Generator, Any

import pytest
from sqlalchemy import text

from tests.sql_connector import get_session_test

@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='module', autouse=True)
async def cleanup():
    tables = [
        'address', 'addresses_for_user', 'city',
        'district', 'fav_cat_for_user', 'fav_rest_for_user',
        'owners', 'restaurants', 'street', 'users'
    ]
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in tables:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()