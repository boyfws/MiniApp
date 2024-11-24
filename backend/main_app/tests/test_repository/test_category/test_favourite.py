from sqlalchemy import text

from src.models.dto.category import CategoryDTO
from src.models.dto.favourites import FavouriteCategoryDTO, AllFavouriteCategoriesRequest, FavouriteCategoryResponse
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.user import UserRequest
from src.repository.category.category import CategoryRepo
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.repository.user import UserRepo
from tests.conftest import get_session_test, cleanup

@pytest.fixture(scope="function")
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'users', 'categories', 'fav_cat_for_user'
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.fixture(scope="function")
async def create_db_values_categories():
    await UserRepo(session_getter=get_session_test).create_user(model=UserRequest(id=1))
    await UserRepo(session_getter=get_session_test).create_user(model=UserRequest(id=2))
    await CategoryRepo(session_getter=get_session_test).create(model=CategoryDTO(name='Бар'))
    await CategoryRepo(session_getter=get_session_test).create(model=CategoryDTO(name='Итальянское'))

@pytest.fixture(scope="function")
async def create_db_values_all_categories(create_db_values_categories):
    await FavouriteCategoryRepo(session_getter=get_session_test).create(FavouriteCategoryDTO(user_id=1, cat_id=1))
    await FavouriteCategoryRepo(session_getter=get_session_test).create(FavouriteCategoryDTO(user_id=1, cat_id=2))
    await FavouriteCategoryRepo(session_getter=get_session_test).create(FavouriteCategoryDTO(user_id=2, cat_id=1))


@pytest.mark.parametrize(
    "model, expected_cat_id, expectation",
    [
        (FavouriteCategoryDTO(user_id=1, cat_id=1), 1, does_not_raise()),
        (FavouriteCategoryDTO(user_id=1, cat_id=2), 2, does_not_raise()),
        (FavouriteCategoryDTO(user_id=2, cat_id=1), 1, does_not_raise())
    ]
)
async def test_create(
        model: FavouriteCategoryDTO,
        expected_cat_id: int,
        expectation: AbstractContextManager,
        create_db_values_categories,
        truncate_db
):
    async with expectation:
        result = await FavouriteCategoryRepo(session_getter=get_session_test).create(model)
        assert result.cat_id == expected_cat_id

@pytest.mark.parametrize(
    "model, expected_cat_id, expectation",
    [
        (FavouriteCategoryDTO(user_id=1, cat_id=1), 1, does_not_raise()),
        (FavouriteCategoryDTO(user_id=1, cat_id=2), 2, does_not_raise()),
        (FavouriteCategoryDTO(user_id=2, cat_id=1), 1, does_not_raise())
    ]
)
async def test_delete(
        model: FavouriteCategoryDTO,
        expected_cat_id: int,
        expectation: AbstractContextManager,
        create_db_values_categories,
        truncate_db
):
    async with expectation:
        result = await FavouriteCategoryRepo(session_getter=get_session_test).delete(model)
        assert result.cat_id == expected_cat_id

@pytest.mark.parametrize(
    "model, expected_list_cat, expectation",
    [
        (AllFavouriteCategoriesRequest(user_id=10000),
         [],
         does_not_raise()),
        (AllFavouriteCategoriesRequest(user_id=1),
         [FavouriteCategoryResponse(cat_id=1), FavouriteCategoryResponse(cat_id=2)],
         does_not_raise()),
        (AllFavouriteCategoriesRequest(user_id=2),
         [FavouriteCategoryResponse(cat_id=1)],
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
        result = await FavouriteCategoryRepo(session_getter=get_session_test).get_all_user_fav_categories(model)
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
        result = await FavouriteCategoryRepo(session_getter=get_session_test).drop_all_user_fav_categories(model)
        assert expected_user_id == result.user_id