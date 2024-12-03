import pytest
from sqlalchemy import text

from src.models.dto.address_for_user import AllAddressesForUser, AddressForUserDTO
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.test_repository.test_address.test_addresses_for_user import create_db_values_1, truncate_db, create_db_values_2

@pytest.mark.parametrize(
    "model",
    [
        AddressForUserDTO(user_id=1, address_id=1)
    ]
)
async def test_add_address_for_user(model: AddressForUserDTO, test_app, create_db_values_1, truncate_db):
    response = await test_app.post('/v1_test/AddressesForUser/add_address/', json=model.model_dump())
    assert response.status_code == 200

@pytest.mark.parametrize(
    "user_id, address_id",
    [
        [1, 1],
        [1, 2]
    ]
)
async def test_delete(user_id: int, address_id: int, test_app, create_db_values_1, truncate_db):
    response = await test_app.delete(f'/v1_test/AddressesForUser/delete_address/{user_id}/{address_id}')
    assert response.status_code == 200

@pytest.mark.parametrize(
    "model, expected_list_result",
    [
        (AllAddressesForUser(user_id=1), [AddressForUserDTO(user_id=1, address_id=1), AddressForUserDTO(user_id=1, address_id=2)]),
        (AllAddressesForUser(user_id=1000), [])
    ]
)
async def test_get_all_user_addresses(
        model: AllAddressesForUser,
        expected_list_result: list[AddressForUserDTO],
        test_app, create_db_values_2, truncate_db): # fixtures
    response = await test_app.get(f'/v1_test/AddressesForUser/get_all_addresses/{model.user_id}')
    assert response.status_code == 200
    assert response.json() == [data.model_dump() for data in expected_list_result]

@pytest.mark.parametrize(
    "model, expected_status",
    [
        (AllAddressesForUser(user_id=1), 200),
        (AllAddressesForUser(user_id=1000), 200)
    ]
)
async def test_drop_all_user_addresses(
        model: AllAddressesForUser,
        expected_status: int,
        test_app, create_db_values_2, truncate_db):
    response = await test_app.delete(f'/v1_test/AddressesForUser/drop_all_addresses/{model.user_id}')
    assert response.status_code == 200
    async with get_session_test() as session:
        count = await session.execute(text(f"SELECT COUNT(*) FROM addresses_for_user WHERE user_id = {model.user_id}"))
        assert count.scalar() == 0