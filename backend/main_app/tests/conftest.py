import pytest
from sqlalchemy import text

from tests.sql_connector import get_session_test

@pytest.fixture(scope='function', autouse=True)
async def cleanup():
    tables = [
        'address', 'addresses_for_user', 'categories', 'city',
        'district', 'fav_cat_for_user', 'fav_rest_for_user',
        'owners', 'restaurants', 'street', 'users'
    ]
    yield
    async with get_session_test() as session_test:
        for table in tables:
            await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
        await session_test.commit()