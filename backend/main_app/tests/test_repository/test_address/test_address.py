import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.address import AddressDTO
from src.repository.address.address import AddressRepo
from tests.conftest import get_session_test, cleanup

@pytest.mark.usefixtures("cleanup")
class TestAddressRepo:
    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (AddressDTO(
                city="Москва",
                district="Измайловский",
                street="улица Вернадского",
                house=11,
                location="SRID=4326;POINT(37.617 55.755)"),
             1,
             does_not_raise())
        ]
    )
    @pytest.mark.asyncio
    async def test_add_address(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        async with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result.id

