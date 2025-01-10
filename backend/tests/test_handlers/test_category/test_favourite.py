import pytest

from src.models.dto.favourites import FavouriteCategoryDTO, FavouriteCategoryResponse, AllFavouriteCategoriesRequest
from tests.common.category import burgers_1, sushi_1, pizza_2
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
    "user_id, cat_id, expected_cat_id",
    [
        (1, 1, 1),
        (1, 2, 2),
        (2, 1, 1)
    ]
)
async def test_delete(
        user_id: int,
        cat_id: int,
        expected_cat_id: int,
        create_db_values_categories,
        truncate_db,
        test_app
):
    response = await test_app.delete(f'/v1_test/FavouriteCategory/delete_fav_category/{user_id}/{cat_id}')
    assert response.status_code == 200
    assert response.json()['cat_id'] == expected_cat_id

@pytest.mark.parametrize(
    "user_id, expected_list_cat",
    [
        (10000, [],),
        (1, [FavouriteCategoryResponse(cat_id=1), FavouriteCategoryResponse(cat_id=2)],),
        (2, [FavouriteCategoryResponse(cat_id=1)],)
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