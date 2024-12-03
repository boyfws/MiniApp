import pytest

from src.models.dto.favourites import FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest, \
    FavouriteRestaurantResponse
from tests.test_handlers.fixtures import test_app
from tests.test_repository.restaurants.test_favourite import create_db_values_restaurants, truncate_db_rest, create_db_values_all_restaurants


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
        truncate_db_rest,
        test_app
):
    response = await test_app.post("/v1_test/FavouriteRestaurant/add_fav_restaurant/", json=model.model_dump())
    assert response.status_code == 200
    assert response.json()['rest_id'] == expected_rest_id

@pytest.mark.parametrize(
    "user_id, rest_id, expected_rest_id",
    [
        (1, 1, 1),
        (1, 2, 2),
        (2, 1, 1)
    ]
)
async def test_delete(
        user_id: int,
        rest_id: int,
        expected_rest_id: int,
        create_db_values_restaurants,
        truncate_db_rest,
        test_app
):
    response = await test_app.delete(f"/v1_test/FavouriteRestaurant/delete_fav_restaurant/{user_id}/{rest_id}")
    assert response.status_code == 200
    assert response.json()['rest_id'] == expected_rest_id

@pytest.mark.parametrize(
    "user_id, expected_list_rest",
    [
        (10000, []),
        (1, [FavouriteRestaurantResponse(rest_id=1), FavouriteRestaurantResponse(rest_id=2)]),
        (2, [FavouriteRestaurantResponse(rest_id=1)])
    ]
)
async def test_get_all_user_fav_restaurants(
        user_id: int,
        expected_list_rest: list[FavouriteRestaurantResponse],
        create_db_values_all_restaurants,
        truncate_db_rest,
        test_app
):
    response = await test_app.get(f"/v1_test/FavouriteRestaurant/get_all_user_fav_restaurants/{user_id}")
    assert response.status_code == 200
    assert response.json() == [data.model_dump() for data in expected_list_rest]

@pytest.mark.parametrize(
    "user_id, expected_user_id",
    [
        (1, 1),
        (2, 2)
    ]
)
async def test_drop_all_user_fav_restaurants(
        user_id: int,
        expected_user_id: int,
        create_db_values_all_restaurants,
        truncate_db_rest,
        test_app
):
    response = await test_app.delete(f"/v1_test/FavouriteRestaurant/drop_all_user_fav_restaurants/{user_id}")
    assert response.status_code == 200
    assert response.json()['user_id'] == expected_user_id