import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.address import AddressDTO
from src.repository.address.address import AddressRepo
from tests.conftest import get_session_test
from tests.common.address import get_addresses

class TestAddressRepo:
    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (get_addresses()[0], 1, does_not_raise()),
            (get_addresses()[1], 2, does_not_raise())
        ]
    )
    async def test_add_address_different_addresses(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result

    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (get_addresses()[2], 3, does_not_raise()),
            (get_addresses()[3], 4, does_not_raise())
        ]
    )
    async def test_add_address_same_city(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result

    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (get_addresses()[2], 3, does_not_raise()),
            (get_addresses()[5], 5, does_not_raise())
        ]
    )
    async def test_add_address_same_city_and_district(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result
