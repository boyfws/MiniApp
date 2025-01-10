import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from sqlalchemy import text, select

from src.models.dto.address_for_user import AddressForUserDTO, AllAddressesForUser
from src.models.dto.user import UserRequest
from src.models.orm.schemas import AddressesForUser
from src.repository.address.address import AddressRepo
from src.repository.address.address_for_user import AddressForUserRepo
from src.repository.user import UserRepo
from tests.conftest import get_session_test
from tests.common.address import get_addresses

ad_repo = AddressRepo(session_getter=get_session_test)
user_repo = UserRepo(session_getter=get_session_test)
ad_user_repo = AddressForUserRepo(session_getter=get_session_test)


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
    await ad_repo.add_address(get_addresses()[1])
    await ad_repo.add_address(get_addresses()[2])
    await user_repo.create_user(1)

@pytest.fixture(scope='function')
async def create_db_values_2():
    # добавили пару различных адресов в базу
    await ad_repo.add_address(get_addresses()[1])
    await ad_repo.add_address(get_addresses()[2])

    # добавили одного юзера в базу с номером 1
    await user_repo.create_user(1)

    # добавили адреса для юзера номера 1
    await ad_user_repo.create(1, 1)
    await ad_user_repo.create(1, 2)

@pytest.mark.parametrize(
    "user_id, address_id, expected_status, expectation",
    [
        (1, 1, 200, does_not_raise()),
        (1, 2, 200, does_not_raise())
    ]
)
async def test_create(user_id: int, address_id: int, expected_status: int, expectation: AbstractContextManager, create_db_values_1, truncate_db):
    async with expectation:
        result = await ad_user_repo.create(user_id, address_id)
        assert expected_status == result.status

@pytest.mark.parametrize(
    'model, expected_status, expected_addresses, expectation',
    [
        (AddressForUserDTO(user_id=1, address_id=1), 200, [AddressForUserDTO(user_id=1, address_id=2)], does_not_raise()),
        (AddressForUserDTO(user_id=1, address_id=2), 200, [AddressForUserDTO(user_id=1, address_id=1)], does_not_raise())
    ]
)
async def test_delete(
        model: AddressForUserDTO,
        expected_status: int,
        expected_addresses: list[AddressForUserDTO],
        expectation: AbstractContextManager,
        create_db_values_2, truncate_db):
    with expectation:
        result = await ad_user_repo.delete(model)
        assert expected_status == result.status
        async with get_session_test() as session:
            stmt = select(AddressesForUser.user_id, AddressesForUser.address_id).where(AddressesForUser.user_id == model.user_id)
            addresses = await session.execute(stmt)
            all_addresses_for_user = [
                AddressForUserDTO.model_validate(address, from_attributes=True) for address in addresses.all()
            ]
            assert all_addresses_for_user == expected_addresses

@pytest.mark.parametrize(
    "model, expected_list_result, expectation",
    [
        (AllAddressesForUser(user_id=1), [AddressForUserDTO(user_id=1, address_id=1), AddressForUserDTO(user_id=1, address_id=2)], does_not_raise()),
        (AllAddressesForUser(user_id=1000), [], does_not_raise())
    ]
)
async def test_get_all_user_addresses(model: AllAddressesForUser, expected_list_result: list[AddressForUserDTO], expectation: AbstractContextManager, create_db_values_2, truncate_db):
    with expectation:
        result = await ad_user_repo.get_all_user_addresses(model)
        assert expected_list_result == result

@pytest.mark.parametrize(
    "model, expected_status, expectation",
    [
        (AllAddressesForUser(user_id=1), 200, does_not_raise()),
        (AllAddressesForUser(user_id=1000), 200, does_not_raise())
    ]
)
async def test_drop_all_user_addresses(model: AllAddressesForUser, expected_status: int, expectation: AbstractContextManager, create_db_values_2, truncate_db):
    with expectation:
        result = await ad_user_repo.drop_all_user_addresses(model)
        assert expected_status == result.status
        assert await ad_user_repo.get_all_user_addresses(model) == []