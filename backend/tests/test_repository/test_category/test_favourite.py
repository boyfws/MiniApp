from sqlalchemy import text

from src.models.dto.favourites import FavouriteCategoryDTO, AllFavouriteCategoriesRequest, FavouriteCategoryResponse
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.repository.user import UserRepo
from tests.common.category import burgers_1, sushi_1, burgers_2, pizza_2
from tests.conftest import get_session_test, cleanup

user_repo = UserRepo(session_getter=get_session_test)

fav_cat_repo = FavouriteCategoryRepo(session_getter=get_session_test)

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

@pytest.fixture(scope="function")
async def create_db_values_categories():
    await user_repo.create_user(1)
    await user_repo.create_user(2)

@pytest.fixture(scope="function")
async def create_db_values_all_categories(create_db_values_categories):
    await fav_cat_repo.create(burgers_1)
    await fav_cat_repo.create(sushi_1)
    await fav_cat_repo.create(burgers_2)


@pytest.mark.parametrize(
    "model, expected_cat_name, expectation",
    [
        (burgers_1, "Бургеры", does_not_raise()),
        (sushi_1, "Суши", does_not_raise()),
        (pizza_2, "Пицца", does_not_raise())
    ]
)
async def test_create(
        model: FavouriteCategoryDTO,
        expected_cat_name: str,
        expectation: AbstractContextManager,
        create_db_values_categories,
        truncate_db
):
    async with expectation:
        result = await fav_cat_repo.create(model)
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
    async with expectation:
        result = await fav_cat_repo.delete(model)
        assert result.cat_name == expected_cat_name

@pytest.mark.parametrize(
    "model, expected_list_cat, expectation",
    [
        (AllFavouriteCategoriesRequest(user_id=10000),
         [],
         does_not_raise()),
        (AllFavouriteCategoriesRequest(user_id=1),
         [FavouriteCategoryResponse(cat_name="Бургеры"), FavouriteCategoryResponse(cat_name="Суши")],
         does_not_raise()),
        (AllFavouriteCategoriesRequest(user_id=2),
         [FavouriteCategoryResponse(cat_name="Бургеры")],
         does_not_raise())
    ]
)
async def test_get_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        expected_list_cat: list[FavouriteCategoryResponse],
        expectation: AbstractContextManager,
        create_db_values_all_categories,
        truncate_db
):
    async with expectation:
        result = await fav_cat_repo.get_all_user_fav_categories(model)
        assert result == expected_list_cat

@pytest.mark.parametrize(
    "model, expected_user_id, expectation",
    [
        (AllFavouriteCategoriesRequest(user_id=1), 1, does_not_raise()),
        (AllFavouriteCategoriesRequest(user_id=2), 2, does_not_raise())
    ]
)
async def test_drop_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        expected_user_id: int,
        expectation: AbstractContextManager,
        create_db_values_all_categories,
        truncate_db
):
    async with expectation:
        result = await fav_cat_repo.drop_all_user_fav_categories(model)
        assert expected_user_id == result.user_id