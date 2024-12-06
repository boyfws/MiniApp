import pytest

from src.models.dto.user import UserRequest
from src.repository.user import UserRepo
from src.service import UserService, OwnerService
from tests.sql_connector import get_session_test
from tests.test_repository.test_user_owner import truncate_db, owner_repo

# @pytest.mark.parametrize(
#     "model, expected_status",
#     [
#         (UserRequest(id=1), 200),
#         (UserRequest(id=20000), 200)
#     ]
# )
# async def test_create_user(
#         model: UserRequest,
#         expected_status: int,
#         truncate_db
# ):
#     result = await UserService(repo=UserRepo(session_getter=get_session_test)).create_user(model)
#     assert expected_status == result.status

owner_service = OwnerService(session_getter=get_session_test)

# async def test_create_owner(truncate_db):
#     await owner_service.create_owner(owner_id=20000)
#     await owner_service.create_owner(owner_id=1)

async def test_is_owner(truncate_db):
    await owner_repo.create_owner(owner_id=1)
    assert await owner_service.is_owner(1)
    assert not await owner_service.is_owner(2)