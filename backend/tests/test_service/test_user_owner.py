from src.service import OwnerService
from tests.sql_connector import get_session_test
from tests.test_repository.test_user_owner import truncate_db, owner_repo



owner_service = OwnerService(session_getter=get_session_test)


async def test_is_owner(truncate_db):
    await owner_repo.create_owner(owner_id=1)
    assert await owner_service.is_owner(1)
    assert not await owner_service.is_owner(2)