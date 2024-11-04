import logging

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from interface import TablesRepositoryInterface, AbstractModel
from src.models.dto.common import Result
from src.models.dto.favourites import FavouriteCategoryUpdateRequest, FavouriteCategoryUpdateResponse
from src.models.orm.category import Category
from src.models.orm.favourites.category import FavouriteCategory


class FavouriteRestaurant(TablesRepositoryInterface):

    def __init__(self, model: FavouriteCategory):
        self.model: FavouriteCategory = model

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteCategoryUpdateRequest
    ) -> AbstractModel:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteCategoryUpdateRequest
    ) -> AbstractModel:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )



    async def get(
            self,
            session: AsyncSession,
            model: AbstractModel
    ) -> AbstractModel:
        return await session.scalars(
            select(self.model)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )