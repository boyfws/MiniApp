from src.repository.tables.favourite_restaurants import FavouriteRestaurantRepo
from src.service.tables.restaurant.favourite import FavouriteRestaurantService


def get_fav_restaurant_service() -> FavouriteRestaurantService:
    return FavouriteRestaurantService(repo=FavouriteRestaurantRepo())

__all__ = [
    "get_fav_restaurant_service", "FavouriteRestaurantService",
]
