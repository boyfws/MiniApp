from sqlalchemy import text

from src.models.dto.favourites import FavouriteCategoryDTO
import pytest
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.repository.user import UserRepo
from tests.common.category import burgers_1, sushi_1, burgers_2, pizza_2
from tests.conftest import get_session_test

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


@pytest.mark.parametrize("model", [burgers_1, sushi_1, pizza_2])
async def test_create(
        model: FavouriteCategoryDTO,
        create_db_values_categories,
        truncate_db
):
    await fav_cat_repo.create(model)

@pytest.mark.parametrize("model", [burgers_1, sushi_1, pizza_2])
async def test_delete(
        model: FavouriteCategoryDTO,
        create_db_values_categories,
        truncate_db
):
    await fav_cat_repo.delete(model)

@pytest.mark.parametrize(
    "user_id, expected_list_cat",
    [
        (10000, []),
        (1, ["Бургеры", "Суши"]),
        (2, ["Бургеры"])
    ]
)
async def test_get_all_user_fav_categories(
        user_id: int,
        expected_list_cat: list[str],
        create_db_values_all_categories,
        truncate_db
):
    result = await fav_cat_repo.get_all_user_fav_categories(user_id)
    assert result == expected_list_cat

@pytest.mark.parametrize("user_id", [1, 2])
async def test_drop_all_user_fav_categories(
        user_id: int,
        create_db_values_all_categories,
        truncate_db
):
    await fav_cat_repo.drop_all_user_fav_categories(user_id)