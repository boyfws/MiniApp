from tests.test_repository.test_user_owner import truncate_db, owner_repo
from tests.test_handlers.fixtures import test_app

async def test_is_owner(truncate_db, test_app):
    await owner_repo.create_owner(owner_id=1)
    response2 = await test_app.get(f"/v1_test/Owner/is_owner/{1}")
    assert response2.status_code == 200
    assert response2.json()
    response3 = await test_app.get(f"/v1_test/Owner/is_owner/{2}")
    assert response3.status_code == 200
    assert not response3.json()