from fastapi import APIRouter, Depends

from src.models.dto.favourites import FavouriteRestaurantDTO
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.user import UserRepo
from src.service.restaurant import FavouriteRestaurantService
from tests.sql_connector import get_session_test

fav_restaurant_router = APIRouter(
    prefix="/FavouriteRestaurant",
    tags=["FavouriteRestaurant"]
)

def get_test_fav_restaurant_service() -> FavouriteRestaurantService:
    return FavouriteRestaurantService(
        repo=FavouriteRestaurantRepo(session_getter=get_session_test),
        user_repo=UserRepo(session_getter=get_session_test)
    )


@fav_restaurant_router.get("/get_all_user_fav_restaurants/{user_id}")
async def get_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_test_fav_restaurant_service)
) -> list[int]:
    return await service.get_all_user_fav_restaurants(user_id)

@fav_restaurant_router.delete("/drop_all_user_fav_restaurants/{user_id}")
async def drop_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_test_fav_restaurant_service)
) -> None:
    return await service.drop_all_user_fav_restaurants(user_id)

@fav_restaurant_router.post("/add_fav_restaurant/")
async def add_fav_restaurant(
        model: FavouriteRestaurantDTO,
        service: FavouriteRestaurantService = Depends(get_test_fav_restaurant_service)
) -> int:
    return await service.create(model)

@fav_restaurant_router.delete("/delete_fav_restaurant/{user_id}/{rest_id}")
async def delete_fav_restaurant(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_test_fav_restaurant_service)
) -> None:
    return await service.delete(FavouriteRestaurantDTO(user_id=user_id, rest_id=rest_id))

@fav_restaurant_router.get("/check_is_favourite/{user_id}/{rest_id}")
async def check_is_favourite(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_test_fav_restaurant_service)
) -> bool:
    return await service.is_favourite(user_id, rest_id)