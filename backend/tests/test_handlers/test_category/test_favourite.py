import pytest
from sqlalchemy import text

from src.models.dto.favourites import FavouriteCategoryDTO, FavouriteCategoryResponse, AllFavouriteCategoriesRequest
from tests.common.category import burgers_1, sushi_1, pizza_2
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.test_repository.test_category.test_favourite import create_db_values_categories, truncate_db, create_db_values_all_categories

@pytest.mark.parametrize(
    "model, expected_cat_name",
    [
        (burgers_1, "Бургеры"),
        (sushi_1, "Суши"),
        (pizza_2, "Пицца")
    ]
)
async def test_create(
        model: FavouriteCategoryDTO,
        expected_cat_name: str,
        create_db_values_categories,
        truncate_db,
        test_app
):
    response = await test_app.post("/v1_test/FavouriteCategory/add_fav_category/", json=model.model_dump())
    assert response.status_code == 200
    assert expected_cat_name == response.json()['cat_name']

@pytest.mark.parametrize(
    "user_id, cat_name, expected_cat_name",
    [
        (1, "Бургеры", "Бургеры"),
        (1, "Суши", "Суши"),
        (2, "Бургеры", "Бургеры")
    ]
)
async def test_delete(
        user_id: int,
        cat_name: str,
        expected_cat_name: str,
        create_db_values_categories,
        truncate_db,
        test_app
):
    response = await test_app.delete(f'/v1_test/FavouriteCategory/delete_fav_category/{user_id}/{cat_name}')
    assert response.status_code == 200
    assert response.json()['cat_name'] == expected_cat_name

@pytest.mark.parametrize(
    "user_id, expected_list_cat",
    [
        (10000, [],),
        (1, [FavouriteCategoryResponse(cat_name="Бургеры"), FavouriteCategoryResponse(cat_name="Суши")],),
        (2, [FavouriteCategoryResponse(cat_name="Бургеры")],)
    ]
)
async def test_get_all_user_fav_categories(
        user_id: int,
        expected_list_cat: list[FavouriteCategoryResponse],
        create_db_values_all_categories,
        truncate_db,
        test_app
):
    response = await test_app.get(f'/v1_test/FavouriteCategory/get_all_user_fav_categories/{user_id}')
    assert response.status_code == 200
    assert response.json() == [data.model_dump() for data in expected_list_cat]

@pytest.mark.parametrize(
    "user_id, expected_user_id",
    [
        (1, 1),
        (2, 2)
    ]
)
async def test_drop_all_user_fav_categories(
        user_id: int,
        expected_user_id: int,
        create_db_values_all_categories,
        truncate_db,
        test_app
):
    response = await test_app.delete(f'/v1_test/FavouriteCategory/drop_all_user_fav_categories/{user_id}')
    assert response.status_code == 200
    assert response.json()['user_id'] == expected_user_id
    async with get_session_test() as session:
        count = await session.execute(text(f"SELECT COUNT(*) FROM fav_cat_for_user WHERE user_id = {user_id}"))
        assert count.scalar() == 0