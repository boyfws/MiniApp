from src.models.dto.favourites import (AllFavouriteRestaurantsRequest, FavouriteRestaurantDTO, FavouriteRestaurantResponse)
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo

class FavouriteRestaurantService:
    def __init__(self, repo: FavouriteRestaurantRepo):
        self.repo = repo
    async def delete(self, model: FavouriteRestaurantDTO) -> FavouriteRestaurantResponse:
        return await self.repo.delete(model)

    async def create(self, model: FavouriteRestaurantDTO) -> FavouriteRestaurantResponse:
        return await self.repo.create(model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> list[FavouriteRestaurantResponse]:
        return await self.repo.get_all_user_fav_restaurants(model)

    async def drop_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        return await self.repo.drop_all_user_fav_restaurants(model)