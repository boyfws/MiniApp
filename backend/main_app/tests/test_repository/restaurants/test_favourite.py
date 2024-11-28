import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from sqlalchemy import text

from src.models.dto.category import CategoryDTO
from src.models.dto.favourites import FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest, \
    FavouriteRestaurantResponse
from src.models.dto.user import UserRequest
from src.repository.category.category import CategoryRepo
from src.repository.owner import OwnerRepo
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.restaurant.restaurant import RestaurantRepo
from src.repository.user import UserRepo
from tests.sql_connector import get_session_test
from tests.test_repository.restaurants.test_restaurant import restaurants

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
                'users', 'restaurants', 'fav_rest_for_user', 'owners', 'categories',
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.fixture(scope="function")
async def create_db_values_restaurants():
    rest_1, rest_2 = restaurants()
    await OwnerRepo(session_getter=get_session_test).create_owner(1)
    await user_repo.create_user(model=UserRequest(id=1))
    await user_repo.create_user(model=UserRequest(id=2))
    await cat_repo.create(model=CategoryDTO(name='Бар'))
    await cat_repo.create(model=CategoryDTO(name='Итальянское'))
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
        assert result.rest_id == expected_rest_id

@pytest.mark.parametrize(
    "model, expected_rest_id, expectation",
    [
        (FavouriteRestaurantDTO(user_id=1, rest_id=1), 1, does_not_raise()),
        (FavouriteRestaurantDTO(user_id=1, rest_id=2), 2, does_not_raise()),
        (FavouriteRestaurantDTO(user_id=2, rest_id=1), 1, does_not_raise())
    ]
)
async def test_delete(
        model: FavouriteRestaurantDTO,
        expected_rest_id: int,
        expectation: AbstractContextManager,
        create_db_values_restaurants,
        truncate_db_rest
):
    with expectation:
        result = await fav_rest_repo.delete(model)
        assert result.rest_id == expected_rest_id

@pytest.mark.parametrize(
    "model, expected_list_rest, expectation",
    [
        (AllFavouriteRestaurantsRequest(user_id=10000),
         [],
         does_not_raise()),
        (AllFavouriteRestaurantsRequest(user_id=1),
         [FavouriteRestaurantResponse(rest_id=1), FavouriteRestaurantResponse(rest_id=2)],
         does_not_raise()),
        (AllFavouriteRestaurantsRequest(user_id=2),
         [FavouriteRestaurantResponse(rest_id=1)],
         does_not_raise())
    ]
)
async def test_get_all_user_fav_restaurants(
        model: AllFavouriteRestaurantsRequest,
        expected_list_rest: list[FavouriteRestaurantResponse],
        expectation: AbstractContextManager,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    async with expectation:
        result = await fav_rest_repo.get_all_user_fav_restaurants(model)
        assert result == expected_list_rest

@pytest.mark.parametrize(
    "model, expected_user_id, expectation",
    [
        (AllFavouriteRestaurantsRequest(user_id=1), 1, does_not_raise()),
        (AllFavouriteRestaurantsRequest(user_id=2), 2, does_not_raise())
    ]
)
async def test_drop_all_user_fav_restaurants(
        model: AllFavouriteRestaurantsRequest,
        expected_user_id: int,
        expectation: AbstractContextManager,
        create_db_values_all_restaurants,
        truncate_db_rest
):
    async with expectation:
        result = await fav_rest_repo.drop_all_user_fav_restaurants(model)
        assert expected_user_id == result.user_id