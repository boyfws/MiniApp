from sqlalchemy import text

from src.models.dto.user import UserRequest
from src.repository.owner import OwnerRepo
from src.repository.user import UserRepo
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

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

@pytest.mark.parametrize(
    "model, expected_status",
    [
        (UserRequest(id=1), 200),
        (UserRequest(id=20000), 200)
    ]
)
async def test_create_user(
        model: UserRequest,
        expected_status: int,
        truncate_db
):
    result = await UserRepo(session_getter=get_session_test).create_user(model)
    assert expected_status == result.status

async def test_create_owner(truncate_db):
    await OwnerRepo(session_getter=get_session_test).create_owner(owner_id=20000)
    await OwnerRepo(session_getter=get_session_test).create_owner(owner_id=1)
