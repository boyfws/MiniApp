from dataclasses import asdict

import pytest
from sqlalchemy import text
from starlette.testclient import TestClient

from src.api import router_v1
from src.app import App
from src.config import configuration
from dataclasses import asdict

from src.database.sql_session import get_session
from src.lifespan import lifespan


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(App(host='localhost',
                   port=8000,
                   lifespan=lifespan,
                   **asdict(configuration.app)
                   ).included_cors().included_routers(routers=[router_v1]))
    yield client

@pytest.fixture(scope="module")
async def truncate_db_api():
    yield
    tables = [
        'address', 'addresses_for_user', 'city',
        'district', 'fav_cat_for_user', 'fav_rest_for_user',
        'owners', 'restaurants', 'street', 'users', 'region'
    ]
    async with get_session() as session_test:
        for table in tables:
            await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
        await session_test.commit()