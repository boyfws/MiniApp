from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from interface import TablesRepositoryInterface
from src.models.dto.favourites import (FavouriteRestaurantRequest, FavouriteRestaurantResponse,
                                       FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest)
from src.models.orm.favourites.restaurant import FavouriteRestaurant


class FavouriteRestaurantRepo(TablesRepositoryInterface):

    def __init__(self, model: FavouriteRestaurant):
        self.model: FavouriteRestaurant = model

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.rest_id == model.rest_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantResponse:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantRequest
    ) -> FavouriteRestaurantDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.rest_id == model.rest_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def drop_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def get_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantDTO:
        await session.scalars(
            select(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...