import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from sqlalchemy import text

from src.models.dto.favourites import FavouriteRestaurantDTO
from src.repository.category.category import CategoryRepo
from src.repository.owner import OwnerRepo
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.restaurant.restaurant import RestaurantRepo
from src.repository.user import UserRepo
from tests.common.restaurants import create
from tests.sql_connector import get_session_test

rest_repo = RestaurantRepo(session_getter=get_session_test)
user_repo = UserRepo(session_getter=get_session_test)
fav_rest_repo = FavouriteRestaurantRepo(session_getter=get_session_test)
cat_repo = CategoryRepo(session_getter=get_session_test)

@pytest.fixture(scope="function")
async def truncate_db_rest():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'users', 'restaurants', 'fav_rest_for_user', 'owners',
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.fixture(scope="function")
async def create_db_values_restaurants():
    rest_1, rest_2 = create()
    await OwnerRepo(session_getter=get_session_test).create_owner(1)
    await user_repo.create_user(1)
    await user_repo.create_user(2)
    await rest_repo.create(model=rest_1)
    await rest_repo.create(model=rest_2)

@pytest.fixture(scope="function")
async def create_db_values_all_restaurants(create_db_values_restaurants):
    await fav_rest_repo.create(FavouriteRestaurantDTO(user_id=1, rest_id=1))
    await fav_rest_repo.create(FavouriteRestaurantDTO(user_id=1, rest_id=2))
    await fav_rest_repo.create(FavouriteRestaurantDTO(user_id=2, rest_id=1))

@pytest.mark.parametrize(
    "model, expected_rest_id, expectation",
    [
        (FavouriteRestaurantDTO(user_id=1, rest_id=1), 1, does_not_raise()),
        (FavouriteRestaurantDTO(user_id=1, rest_id=2), 2, does_not_raise()),
        (FavouriteRestaurantDTO(user_id=2, rest_id=1), 1, does_not_raise())
    ]
)
async def test_create(
        model: FavouriteRestaurantDTO,
        expected_rest_id: int,
        expectation: AbstractContextManager,
        create_db_values_restaurants,
        truncate_db_rest
):
    with expectation:
        result = await fav_rest_repo.create(model)
        assert result == expected_rest_id

@pytest.mark.parametrize(
    "model",
    [
        FavouriteRestaurantDTO(user_id=1, rest_id=1),
        FavouriteRestaurantDTO(user_id=1, rest_id=2),
        FavouriteRestaurantDTO(user_id=2, rest_id=1)
    ]
)
async def test_delete(
        model: FavouriteRestaurantDTO,
        create_db_values_restaurants,
        truncate_db_rest
):
    await fav_rest_repo.delete(model)

@pytest.mark.parametrize(
    "user_id, expected_list_rest, expectation",
    [
        (10000, [], does_not_raise()),
        (1, [1, 2], does_not_raise()),
        (2, [1], does_not_raise())
    ]
)
async def test_get_all_user_fav_restaurants(
        user_id: int,
        expected_list_rest: list[int],
        expectation: AbstractContextManager,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    with expectation:
        result = await fav_rest_repo.get_all_user_fav_restaurants(user_id)
        assert result == expected_list_rest

@pytest.mark.parametrize("user_id", [1, 2])
async def test_drop_all_user_fav_restaurants(
        user_id: int,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    await fav_rest_repo.drop_all_user_fav_restaurants(user_id)

@pytest.mark.parametrize(
    "user_id, rest_id, expectation",
    [
        (1, 1, does_not_raise()),
        (1, 2, does_not_raise()),
        (2, 1, does_not_raise()),
        (3, 1, pytest.raises(AssertionError)),
        (3000, 11111, pytest.raises(AssertionError))
    ]
)
async def test_is_favourite(
        user_id: int,
        rest_id: int,
        expectation: AbstractContextManager,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    with expectation:
        result = await fav_rest_repo.is_favourite(user_id, rest_id)
        assert result