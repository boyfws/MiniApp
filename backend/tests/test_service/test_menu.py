from contextlib import AbstractContextManager, nullcontext as does_not_raise
from typing import Optional

import pytest

from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID
from src.service import MenuService
from tests.common.menu import get_menus
from tests.mongo_connector import get_test_db

@pytest.mark.parametrize(
    "model",
    [get_menus()[0], get_menus()[1]]
)
async def test_update_menu(model: MenuDTO):
    await MenuService(session_getter=get_test_db).update_menu_by_rest_id(model)


@pytest.mark.parametrize(
    "model, expected_dto",
    [
        (
            RestaurantRequestUsingID(rest_id=1, user_id=1),
            get_menus()[0]
        ),
        (
            RestaurantRequestUsingID(rest_id=2, user_id=1),
            get_menus()[1]
        ),
        (
            RestaurantRequestUsingID(rest_id=4000, user_id=1),
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
    "model",
    [
        RestaurantRequestUsingID(rest_id=1, user_id=1),
        RestaurantRequestUsingID(rest_id=4, user_id=1),
        RestaurantRequestUsingID(rest_id=2, user_id=1)
    ]
)
async def test_delete_menu_by_rest_id(
        model: RestaurantRequestUsingID,
):
    await MenuService(session_getter=get_test_db).delete_menu_by_rest_id(model)

async def test_empty_database():
    """После выполнения всех тестов тестовая база пустая"""
    async with get_test_db() as session:
        document_count = await session.menu.count_documents({})
    assert document_count == 0