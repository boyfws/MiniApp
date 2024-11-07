from src.database.sql_session import get_session
from src.models.dto.favourites import (AllFavouriteRestaurantsRequest, FavouriteRestaurantDTO,
                                                FavouriteRestaurantResponse, FavouriteRestaurantRequest)
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.service.interface import ServiceInterface

class FavouriteRestaurantService(ServiceInterface):
    def __init__(self, repo: FavouriteRestaurantRepo):
        self.repo = repo
    async def delete(self, model: FavouriteRestaurantRequest) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def update(self, model: FavouriteRestaurantRequest) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.update(session, model)

    async def get(self, model: FavouriteRestaurantRequest) -> FavouriteRestaurantDTO:
        async with get_session() as session:
            return await self.repo.get(session, model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantDTO:
        async with get_session() as session:
            return await self.repo.get_all_user_fav_restaurants(session, model)

    async def drop_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        async with get_session() as session:
            return await self.repo.drop_all_user_fav_restaurants(session, model)