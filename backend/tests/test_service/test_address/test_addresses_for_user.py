import pytest
from sqlalchemy import text

from src.models.dto.address_for_user import AddressForUserDTO, AllAddressesForUser
from src.service.address import AddressesForUserService
from tests.sql_connector import get_session_test
from tests.test_repository.test_address.test_addresses_for_user import create_db_values_1, create_db_values_2

address_for_user_service = AddressesForUserService(session_getter=get_session_test)

@pytest.fixture()
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'users', 'address', 'district', 'city', 'street', 'addresses_for_user', 'region'
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()


@pytest.mark.parametrize(
    "model, expected_status",
    [
        (AddressForUserDTO(user_id=1, address_id=1), 200),
        (AddressForUserDTO(user_id=1, address_id=2), 200)
    ]
)
async def test_create(model: AddressForUserDTO, expected_status: int, create_db_values_1, truncate_db):
    result = await address_for_user_service.create(model)
    assert result.status == expected_status


@pytest.mark.parametrize(
    'model, expected_status',
    [
        (AddressForUserDTO(user_id=1, address_id=1), 200),
        (AddressForUserDTO(user_id=1, address_id=2), 200)
    ]
)
async def test_delete(model: AddressForUserDTO, expected_status: int, create_db_values_1, truncate_db):
    result = await address_for_user_service.delete(model)
    assert result.status == expected_status


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
        create_db_values_2, truncate_db): # fixtures
    result = await address_for_user_service.get_all_user_fav_restaurants(model)
    assert result == expected_list_result

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
        create_db_values_2, truncate_db):
    result = await address_for_user_service.drop_all_user_fav_restaurants(model)
    assert result.status == expected_status
