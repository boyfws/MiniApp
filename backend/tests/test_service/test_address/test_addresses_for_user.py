import pytest
from sqlalchemy import text

from src.models.dto.address import AddressDTO
from src.models.dto.address_for_user import DeleteAddressForUser
from src.service.address import AddressesForUserService
from tests.common.address import get_addresses
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
    "user_id, model",
    [
        (1, get_addresses()[1]),
        (1, get_addresses()[2]),
    ]
)
async def test_create_if_address_exists(
        user_id: int,
        model: AddressDTO,
        create_db_values_1, truncate_db
):
    await address_for_user_service.create(user_id, model)
    all_addresses = await address_for_user_service.repo.get_all_user_addresses(user_id)
    addresses_geo = []
    for address in all_addresses:
        addresses_geo.append(await address_for_user_service.address_repo.get(address.address_id))
    assert addresses_geo == [model]

@pytest.mark.parametrize(
    "user_id, model",
    [
        (1, get_addresses()[1]),
        (1, get_addresses()[2]),
    ]
)
async def test_create_if_address_new(
        user_id: int,
        model: AddressDTO,
        truncate_db
):
    await address_for_user_service.create(user_id, model)
    all_addresses = await address_for_user_service.repo.get_all_user_addresses(user_id)
    addresses_geo = []
    for address in all_addresses:
        addresses_geo.append(await address_for_user_service.address_repo.get(address.address_id))
    assert addresses_geo == [model]



@pytest.mark.parametrize(
    'model, expected_list_result',
    [
        (DeleteAddressForUser(user_id=1, **get_addresses()[1].model_dump()), [get_addresses()[2]]),
        (DeleteAddressForUser(user_id=1, **get_addresses()[2].model_dump()), [get_addresses()[1]])
    ]
)
async def test_delete(
        model: DeleteAddressForUser,
        expected_list_result: list[AddressDTO],
        create_db_values_2, truncate_db):
    await address_for_user_service.delete(model)
    result = await address_for_user_service.get_all_user_addresses(model.user_id)
    assert result == expected_list_result

@pytest.mark.parametrize(
    "user_id, expected_list_result",
    [
        (1, [get_addresses()[1], get_addresses()[2]]),
        (1000, [])
    ]
)
async def test_get_all_user_addresses(
        user_id: int,
        expected_list_result: list[AddressDTO],
        create_db_values_2, truncate_db): # fixtures
    result = await address_for_user_service.get_all_user_addresses(user_id)
    assert result == expected_list_result

@pytest.mark.parametrize("user_id", [1, 1000])
async def test_drop_all_user_addresses(
        user_id: int,
        create_db_values_2, truncate_db):
    await address_for_user_service.drop_all_user_fav_restaurants(user_id)
    result = await address_for_user_service.get_all_user_addresses(user_id)
    assert result == []
