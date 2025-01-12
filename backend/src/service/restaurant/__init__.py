from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.user import UserRepo
from src.service.restaurant.favourite import FavouriteRestaurantService
from src.service.restaurant.restaurant import RestaurantService

def get_fav_restaurant_service() -> FavouriteRestaurantService:
    return FavouriteRestaurantService(repo=FavouriteRestaurantRepo(), user_repo=UserRepo())

def get_restaurant_service() -> RestaurantService:
    return RestaurantService()

__all__ = [
    "get_fav_restaurant_service", "FavouriteRestaurantService",
    "get_restaurant_service", "RestaurantService"
]
