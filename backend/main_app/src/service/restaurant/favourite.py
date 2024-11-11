from src.database.sql_session import get_session
from src.models.dto.favourites import (AllFavouriteRestaurantsRequest, FavouriteRestaurantDTO, FavouriteRestaurantResponse)
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo

class FavouriteRestaurantService:
    def __init__(self, repo: FavouriteRestaurantRepo):
        self.repo = repo
    async def delete(self, model: FavouriteRestaurantDTO) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def create(self, model: FavouriteRestaurantDTO) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.create(session, model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> list[FavouriteRestaurantResponse]:
        async with get_session() as session:
            return await self.repo.get_all_user_fav_restaurants(session, model)

    async def drop_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.drop_all_user_fav_restaurants(session, model)