from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interface import TablesRepositoryInterface
from src.models.dto.favourites import (FavouriteRestaurantRequest, FavouriteRestaurantResponse,
                                                FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest)
from src.models.orm.schemas import FavRestForUser


class FavouriteRestaurantRepo:

    def __init__(self) -> None:
        self.model: FavRestForUser = FavRestForUser()

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantResponse:
        return FavouriteRestaurantResponse()

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantResponse:
        return FavouriteRestaurantResponse()

    async def get(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantDTO:
        return FavouriteRestaurantDTO()

    async def drop_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        return FavouriteRestaurantResponse()

    async def get_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantDTO:
        return FavouriteRestaurantDTO()