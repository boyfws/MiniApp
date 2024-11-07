from fastapi import APIRouter, Depends

from src.models.dto.favourites import AllFavouriteRestaurantsRequest, FavouriteRestaurantResponse, \
    FavouriteRestaurantRequest, FavouriteRestaurantDTO
from src.service.restaurant import get_fav_restaurant_service, FavouriteRestaurantService

fav_restaurant_router = APIRouter(
    prefix="/FavouriteRestaurant",
    tags=["FavouriteRestaurant"]
)

@fav_restaurant_router.get("/get_all_user_fav_restaurants/")
async def get_all_user_fav_restaurants(
        model: AllFavouriteRestaurantsRequest,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantDTO:
    return await service.get_all_user_fav_restaurants(model=model)

@fav_restaurant_router.delete("/drop_all_user_fav_restaurants/")
async def drop_all_user_fav_restaurants(
        model: AllFavouriteRestaurantsRequest,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantResponse:
    return await service.drop_all_user_fav_restaurants(model=model)

@fav_restaurant_router.post("/add_fav_restaurant/")
async def add_fav_restaurant(
        model: FavouriteRestaurantRequest,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantResponse:
    return await service.update(model)

@fav_restaurant_router.delete("/delete_fav_restaurant/")
async def delete_fav_restaurant(
        model: FavouriteRestaurantRequest,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantResponse:
    return await service.delete(model)

@fav_restaurant_router.get("/get_fav_restaurant/")
async def get_fav_restaurant(
        model: FavouriteRestaurantRequest,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> FavouriteRestaurantDTO:
    return await service.get(model)