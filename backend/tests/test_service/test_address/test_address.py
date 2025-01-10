import pytest
from sqlalchemy import text

from src.models.dto.address import AddressDTO
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
