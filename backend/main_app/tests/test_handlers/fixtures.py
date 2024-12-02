import asyncio

import pytest
import uvicorn
from sqlalchemy import text
from httpx import AsyncClient
from src.api import router_v1
from src.app import App
from src.config import configuration
from dataclasses import asdict

from src.database.sql_session import get_session
from src.lifespan import lifespan


@pytest.fixture(scope="module")
async def test_app():
    app = App(
        host='localhost',
        port=8000,
        lifespan=lifespan,
        **asdict(configuration.app)
    ).included_cors().included_routers(routers=[router_v1])

    config = uvicorn.Config(app, host="localhost", port=8000, log_level="info", lifespan="on")
    server = uvicorn.Server(config)

    async def run_server():
        await server.serve()

    server_task = asyncio.create_task(run_server())
    await asyncio.sleep(1)

    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client

    server.should_exit = True  # Graceful shutdown
    await server_task

@pytest.fixture(scope="function")
async def truncate_db_api():
    try:
        yield
    finally:
        tables = [
            'address', 'addresses_for_user', 'city',
            'district', 'fav_cat_for_user', 'fav_rest_for_user',
            'owners', 'restaurants', 'street', 'users', 'region'
        ]
        async with get_session() as session_test:
            for table in tables:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()