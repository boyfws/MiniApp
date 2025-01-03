from typing import Optional

from src.models.dto.menu import MenuDTO, Category, Item
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.restaurant import RestaurantRequestUsingID
from src.repository.menu import MenuRepository
from tests.mongo_connector import get_test_db

vine = Item(Name='Белое вино', Price=[375, 1500], Condition='цена за бокал и бутылку')
cocktails = Item(Name='Коктейли', Price=[500], Description='Авторские коктейли от бармена', Condition='покупка от 3 коктейлей')
drinks = Category(category_name='Напитки', items=[vine, cocktails])
burgers = Item(Name='Чизбургер комбо', Price=[500, 600, 700], Condition='цена за комбо s, m, l')
food = Category(category_name='Бургеры', items=[burgers])

@pytest.mark.parametrize(
    "model, expected_id, expectation",
    [
        (
            MenuDTO(
                restaurant_id=1,
                categories=[drinks],
                restaurant_description='ресторан где можно выпить вино и коктейли'
            ), 1, does_not_raise()
        ),
        (
            MenuDTO(
                restaurant_id=2,
                categories=[food],
                restaurant_description='бургерная'
            ), 2, does_not_raise()
        ),
    ]
)
async def test_update_menu(model: MenuDTO, expected_id: int, expectation: AbstractContextManager):
    async with expectation:
        rest_id = await MenuRepository(session_getter=get_test_db).update_menu_by_rest_id(model)
        assert rest_id == expected_id


@pytest.mark.parametrize(
    "model, expected_dto, expectation",
    [
        (
            RestaurantRequestUsingID(rest_id=1, user_id=1),
            MenuDTO(
                restaurant_id=1,
                categories=[drinks],
                restaurant_description='ресторан где можно выпить вино и коктейли'
            ),
            does_not_raise()
        ),
        (
            RestaurantRequestUsingID(rest_id=2, user_id=1),
            MenuDTO(
                restaurant_id=2,
                categories=[food],
                restaurant_description='бургерная'
            ),
            does_not_raise()
        ),
        (
            RestaurantRequestUsingID(rest_id=4000, user_id=1),
            None,
            does_not_raise()
        )
    ]
)
async def test_get_menu_by_rest_id(
        model: RestaurantRequestUsingID,
        expected_dto: Optional[MenuDTO],
        expectation: AbstractContextManager
):
    async with expectation:
        result = await MenuRepository(session_getter=get_test_db).get_menu_by_rest_id(model)
        assert result == expected_dto

@pytest.mark.parametrize(
    "model, expectation",
    [
        (RestaurantRequestUsingID(rest_id=1, user_id=1), does_not_raise()),
        (RestaurantRequestUsingID(rest_id=4, user_id=1), pytest.raises(AssertionError)),
        (RestaurantRequestUsingID(rest_id=2, user_id=1), does_not_raise())
    ]
)
async def test_delete_menu_by_rest_id(
        model: RestaurantRequestUsingID,
        expectation: AbstractContextManager
):
    with expectation:
        result = await MenuRepository(session_getter=get_test_db).delete_menu_by_rest_id(model)
        assert result

async def test_empty_database():
    """После выполнения всех тестов тестовая база пустая"""
    async with get_test_db() as session:
        document_count = await session.menu.count_documents({})
    assert document_count == 0