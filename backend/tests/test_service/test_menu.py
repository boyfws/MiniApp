from contextlib import AbstractContextManager, nullcontext as does_not_raise
from typing import Optional

import pytest

from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID
from src.service import MenuService
from tests.common.menu import get_menus
from tests.mongo_connector import get_test_db

@pytest.mark.parametrize(
    "model, expected_id",
    [(get_menus()[0], 1), (get_menus()[1], 2),]
)
async def test_update_menu(model: MenuDTO, expected_id: int):
    rest_id = await MenuService(session_getter=get_test_db).update_menu_by_rest_id(model)
    assert rest_id == expected_id


@pytest.mark.parametrize(
    "model, expected_dto",
    [
        (
            RestaurantRequestUsingID(rest_id=1),
            get_menus()[0]
        ),
        (
            RestaurantRequestUsingID(rest_id=2),
            get_menus()[1]
        ),
        (
            RestaurantRequestUsingID(rest_id=4000),
            None
        )
    ]
)
async def test_get_menu_by_rest_id(
        model: RestaurantRequestUsingID,
        expected_dto: Optional[MenuDTO]
):
    result = await MenuService(session_getter=get_test_db).get_menu_by_rest_id(model)
    assert result == expected_dto

@pytest.mark.parametrize(
    "model, expectation",
    [
        (RestaurantRequestUsingID(rest_id=1), does_not_raise()),
        (RestaurantRequestUsingID(rest_id=4), pytest.raises(AssertionError)),
        (RestaurantRequestUsingID(rest_id=2), does_not_raise())
    ]
)
async def test_delete_menu_by_rest_id(
        model: RestaurantRequestUsingID,
        expectation: AbstractContextManager
):
    with expectation:
        result = await MenuService(session_getter=get_test_db).delete_menu_by_rest_id(model)
        assert result

async def test_empty_database():
    """После выполнения всех тестов тестовая база пустая"""
    async with get_test_db() as session:
        document_count = await session.menu.count_documents({})
    assert document_count == 0