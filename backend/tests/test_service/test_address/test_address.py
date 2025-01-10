import pytest
from sqlalchemy import text

from src.models.dto.address import AddressDTO, AddressRequest
from src.repository.address.address import AddressRepo
from src.service.address import AddressService
from tests.common.address import get_addresses
from tests.conftest import get_session_test
address_service = AddressService(repo=AddressRepo(session_getter=get_session_test))


@pytest.fixture()
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'address', 'district', 'city', 'street', 'region'
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.mark.parametrize(
    "model, expected_id",
    [(get_addresses()[0], 1), (get_addresses()[1], 1)]
)
async def test_add_and_delete_address(model: AddressDTO, expected_id: int, truncate_db):
    result = await address_service.add_address(model)
    assert result == expected_id
    await address_service.delete((AddressRequest(id=expected_id)))
