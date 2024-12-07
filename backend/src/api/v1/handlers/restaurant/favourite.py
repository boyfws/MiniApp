from fastapi import APIRouter, Depends

from src.models.dto.favourites import AllFavouriteRestaurantsRequest, FavouriteRestaurantResponse, FavouriteRestaurantDTO
from src.service.restaurant import get_fav_restaurant_service, FavouriteRestaurantService

fav_restaurant_router = APIRouter(
    prefix="/FavouriteRestaurant",
    tags=["FavouriteRestaurant"]
)

@fav_restaurant_router.get("/get_all_user_fav_restaurants/{user_id}")
async def get_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> list[FavouriteRestaurantResponse]:
    return await service.get_all_user_fav_restaurants(model=AllFavouriteRestaurantsRequest(user_id=user_id))

@fav_restaurant_router.delete("/drop_all_user_fav_restaurants/{user_id}")
async def drop_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> AllFavouriteRestaurantsRequest:
    return await service.drop_all_user_fav_restaurants(model=AllFavouriteRestaurantsRequest(user_id=user_id))

@fav_restaurant_router.post("/add_fav_restaurant/")
async def add_fav_restaurant(
        model: FavouriteRestaurantDTO,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantResponse:
    return await service.create(model)

@fav_restaurant_router.delete("/delete_fav_restaurant/{user_id}/{rest_id}")
async def delete_fav_restaurant(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantResponse:
    return await service.delete(FavouriteRestaurantDTO(user_id=user_id, rest_id=rest_id))

@fav_restaurant_router.get("/check_is_favourite/{user_id}/{rest_id}")
async def check_is_favourite(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> bool:
    return await service.is_favourite(user_id, rest_id)