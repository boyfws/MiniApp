import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from sqlalchemy import text

from src.models.dto.address_for_user import AddressForUserDTO, AllAddressesForUser
from src.models.dto.user import UserRequest
from src.repository.address.address import AddressRepo
from src.repository.address.address_for_user import AddressForUserRepo
from src.repository.user import UserRepo
from tests.conftest import get_session_test
from tests.common.address import get_addresses

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

@pytest.fixture(scope="function")
async def create_db_values_1():
    await AddressRepo(session_getter=get_session_test).add_address(get_addresses()[1])
    await AddressRepo(session_getter=get_session_test).add_address(get_addresses()[2])
    await UserRepo(session_getter=get_session_test).create_user(1)

@pytest.fixture(scope='function')
async def create_db_values_2():
    # добавили пару различных адресов в базу
    await AddressRepo(session_getter=get_session_test).add_address(get_addresses()[1])
    await AddressRepo(session_getter=get_session_test).add_address(get_addresses()[2])

    # добавили одного юзера в базу с номером 1
    await UserRepo(session_getter=get_session_test).create_user(1)

    # добавили адреса для юзера номера 1
    model1 = AddressForUserDTO(user_id=1, address_id=1)
    model2 = AddressForUserDTO(user_id=1, address_id=2)
    await AddressForUserRepo(session_getter=get_session_test).create(model1)
    await AddressForUserRepo(session_getter=get_session_test).create(model2)

@pytest.mark.parametrize(
    "model, expected_status, expectation",
    [
        (AddressForUserDTO(user_id=1, address_id=1), 200, does_not_raise()),
        (AddressForUserDTO(user_id=1, address_id=2), 200, does_not_raise())
    ]
)
async def test_create(model: AddressForUserDTO, expected_status: int, expectation: AbstractContextManager, create_db_values_1, truncate_db):
    async with expectation:
        result = await AddressForUserRepo(session_getter=get_session_test).create(model)
        assert expected_status == result.status

@pytest.mark.parametrize(
    'model, expected_status, expectation',
    [
        (AddressForUserDTO(user_id=1, address_id=1), 200, does_not_raise()),
        (AddressForUserDTO(user_id=1, address_id=2), 200, does_not_raise())
    ]
)
async def test_delete(model: AddressForUserDTO, expected_status: int, expectation: AbstractContextManager, create_db_values_1, truncate_db):
    async with expectation:
        result = await AddressForUserRepo(session_getter=get_session_test).delete(model)
        assert expected_status == result.status

@pytest.mark.parametrize(
    "model, expected_list_result, expectation",
    [
        (AllAddressesForUser(user_id=1), [AddressForUserDTO(user_id=1, address_id=1), AddressForUserDTO(user_id=1, address_id=2)], does_not_raise()),
        (AllAddressesForUser(user_id=1000), [], does_not_raise())
    ]
)
async def test_get_all_user_addresses(model: AllAddressesForUser, expected_list_result: list[AddressForUserDTO], expectation: AbstractContextManager, create_db_values_2, truncate_db):
    async with expectation:
        result = await AddressForUserRepo(session_getter=get_session_test).get_all_user_addresses(model)
        assert expected_list_result == result

@pytest.mark.parametrize(
    "model, expected_status, expectation",
    [
        (AllAddressesForUser(user_id=1), 200, does_not_raise()),
        (AllAddressesForUser(user_id=1000), 200, does_not_raise())
    ]
)
async def test_drop_all_user_addresses(model: AllAddressesForUser, expected_status: int, expectation: AbstractContextManager, create_db_values_2, truncate_db):
    async with expectation:
        result = await AddressForUserRepo(session_getter=get_session_test).drop_all_user_addresses(model)
        assert expected_status == result.status