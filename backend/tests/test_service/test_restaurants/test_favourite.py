import pytest
from sqlalchemy import text
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from src.models.dto.favourites import FavouriteRestaurantDTO
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.user import UserRepo
from src.service.restaurant import FavouriteRestaurantService
from tests.sql_connector import get_session_test
from tests.test_repository.test_restaurants.test_favourite import create_db_values_restaurants, create_db_values_all_restaurants

fav_rest_service = FavouriteRestaurantService(
    FavouriteRestaurantRepo(get_session_test),
    UserRepo(get_session_test)
)


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


@pytest.mark.parametrize(
    "model, expected_rest_id",
    [
        (FavouriteRestaurantDTO(user_id=1, rest_id=1), 1),
        (FavouriteRestaurantDTO(user_id=1, rest_id=2), 2),
        (FavouriteRestaurantDTO(user_id=2, rest_id=1), 1)
    ]
)
async def test_create(
        model: FavouriteRestaurantDTO,
        expected_rest_id: int,
        create_db_values_restaurants,
        truncate_db_rest
):
    result = await fav_rest_service.create(model)
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
    await fav_rest_service.delete(model)

@pytest.mark.parametrize(
    "user_id, expected_list_rest",
    [
        (10000, []),
        (1, [1, 2]),
        (2, [1])
    ]
)
async def test_get_all_user_fav_restaurants(
        user_id: int,
        expected_list_rest: list[int],
        create_db_values_all_restaurants,
        truncate_db_rest
):
    result = await fav_rest_service.get_all_user_fav_restaurants(user_id)
    assert result == expected_list_rest

@pytest.mark.parametrize("user_id", [1, 2])
async def test_drop_all_user_fav_restaurants(
        user_id: int,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    await fav_rest_service.drop_all_user_fav_restaurants(user_id)

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
        result = await fav_rest_service.is_favourite(user_id, rest_id)
        assert result