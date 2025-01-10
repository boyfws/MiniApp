from sqlalchemy import text

from src.repository.owner import OwnerRepo
from src.repository.user import UserRepo
import pytest
from tests.sql_connector import get_session_test


@pytest.fixture(scope="function")
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'users', 'owners'
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.mark.parametrize("user_id", [1, 20000])
async def test_create_user(
        user_id: int,
        truncate_db
):
    await UserRepo(session_getter=get_session_test).create_user(user_id)

owner_repo = OwnerRepo(session_getter=get_session_test)

async def test_create_owner(truncate_db):
    await owner_repo.create_owner(owner_id=20000)
    await owner_repo.create_owner(owner_id=1)

async def test_is_owner(truncate_db):
    await owner_repo.create_owner(owner_id=1)
    assert await owner_repo.is_owner(1)
    assert not await owner_repo.is_owner(2)