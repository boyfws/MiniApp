import pytest

from src.models.dto.user import UserRequest
from tests.test_repository.test_user_owner import truncate_db, owner_repo
from tests.test_handlers.fixtures import test_app

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
#         truncate_db,
#         test_app
# ):
#     result = await test_app.post("/v1_test/User/create_user/", json=model.model_dump())
#     assert result.status_code == expected_status

# async def test_create_owner(truncate_db, test_app):
#     response1 = await test_app.post(f"/v1_test/Owner/create_owner/{200000}")
#     assert response1.status_code == 200
#     response2 = await test_app.post(f"/v1_test/Owner/create_owner/{1}")
#     assert response2.status_code == 200

async def test_is_owner(truncate_db, test_app):
    await owner_repo.create_owner(owner_id=1)
    response2 = await test_app.get(f"/v1_test/Owner/is_owner/{1}")
    assert response2.status_code == 200
    assert response2.json()
    response3 = await test_app.get(f"/v1_test/Owner/is_owner/{2}")
    assert response3.status_code == 200
    assert not response3.json()