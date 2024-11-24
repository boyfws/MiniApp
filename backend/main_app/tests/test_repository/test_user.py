from sqlalchemy import text

from src.models.dto.user import UserRequest
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
                'users',
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.mark.parametrize(
    "model, expected_status, expectation",
    [
        (UserRequest(id=1), 200, does_not_raise()),
        (UserRequest(id=20000), 200, does_not_raise())
    ]
)
async def test_create(
        model: UserRequest,
        expected_status: int,
        expectation: AbstractContextManager,
        truncate_db
):
    async with expectation:
        result = await UserRepo(session_getter=get_session_test).create_user(model)
        assert expected_status == result.status
