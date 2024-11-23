import asyncio

import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.address import AddressDTO, AddressRequest, AddressResult
from src.repository.address.address import AddressRepo
from tests.conftest import get_session_test, cleanup


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
             does_not_raise()),
            (AddressDTO(
                city="Санкт-Петербург",
                district="Красноярск",
                street="улица Аникутина",
                house=12,
                location="SRID=4326;POINT(37.617 55.755)"),
            2,
            does_not_raise()
            )
        ]
    )
    async def test_add_address_different_addresses(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result.id

    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (AddressDTO(
                city="Москва",
                district="Измайловский",
                street="улица Вернадского",
                house=50,
                location="SRID=4326;POINT(37.617 55.755)"),
             3,
             does_not_raise()),
            (AddressDTO(
                city="Москва",
                district="Калининский",
                street="улица Аникутина",
                house=13,
                location="SRID=4326;POINT(37.617 55.755)"),
             4,
             does_not_raise()
            )
        ]
    )
    async def test_add_address_same_city(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result.id

    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (AddressDTO(
                city="Москва",
                district="Измайловский",
                street="улица Вернадского",
                house=50,
                location="SRID=4326;POINT(37.617 55.755)"),
             5,
             does_not_raise()),
            (AddressDTO(
                city="Москва",
                district="Измайловский",
                street="улица Аникутина",
                house=13,
                location="SRID=4326;POINT(37.617 55.755)"),
             6,
             does_not_raise()
            )
        ]
    )
    async def test_add_address_same_city_and_district(self, model: AddressDTO, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).add_address(model)
            assert expected_id == result.id

    @pytest.mark.parametrize(
        "model, expected_id, expectation",
        [
            (AddressRequest(id=1),
             1,
             does_not_raise()),
            (AddressRequest(id=2),
             2,
             does_not_raise()
            )
        ]
    )
    async def test_delete_address(self, model: AddressRequest, expected_id: int, expectation: AbstractContextManager):
        with expectation:
            result = await AddressRepo(session_getter=get_session_test).delete(model)
            assert expected_id == result.id
