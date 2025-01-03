import pytest
from sqlalchemy import text

from contextlib import nullcontext as does_not_raise, AbstractContextManager
from src.models.dto.favourites import FavouriteCategoryDTO, AllFavouriteCategoriesRequest, FavouriteCategoryResponse
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.service.category import FavouriteCategoriesService
from tests.sql_connector import get_session_test
from tests.test_repository.test_category.test_favourite import create_db_values_categories, create_db_values_all_categories
from tests.common.category import burgers_1, sushi_1, burgers_2, pizza_2


fav_cat_service = FavouriteCategoriesService(repo=FavouriteCategoryRepo(session_getter=get_session_test))

@pytest.fixture(scope="function")
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'users', 'fav_cat_for_user'
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()


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
        truncate_db
):
    result = await fav_cat_service.create(model)
    assert result.cat_name == expected_cat_name

@pytest.mark.parametrize(
    "model, expected_cat_name, expectation",
    [
        (burgers_1, "Бургеры", does_not_raise()),
        (sushi_1, "Суши", does_not_raise()),
        (burgers_2, "Бургеры", does_not_raise())
    ]
)
async def test_delete(
        model: FavouriteCategoryDTO,
        expected_cat_name: str,
        expectation: AbstractContextManager,
        create_db_values_categories,
        truncate_db
):
    result = await fav_cat_service.delete(model)
    assert result.cat_name == expected_cat_name

@pytest.mark.parametrize(
    "model, expected_list_cat",
    [
        (AllFavouriteCategoriesRequest(user_id=10000), [],),
        (AllFavouriteCategoriesRequest(user_id=1),
         [FavouriteCategoryResponse(cat_name="Бургеры"), FavouriteCategoryResponse(cat_name="Суши")],),
        (AllFavouriteCategoriesRequest(user_id=2),
         [FavouriteCategoryResponse(cat_name="Бургеры")],)
    ]
)
async def test_get_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        expected_list_cat: list[FavouriteCategoryResponse],
        create_db_values_all_categories,
        truncate_db
):
    result = await fav_cat_service.get_all_user_fav_categories(model)
    assert result == expected_list_cat

@pytest.mark.parametrize(
    "model, expected_user_id",
    [
        (AllFavouriteCategoriesRequest(user_id=1), 1),
        (AllFavouriteCategoriesRequest(user_id=2), 2)
    ]
)
async def test_drop_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        expected_user_id: int,
        create_db_values_all_categories,
        truncate_db
):
    result = await fav_cat_service.drop_all_user_fav_categories(model)
    assert result.user_id == expected_user_id