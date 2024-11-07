from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interface import TablesRepositoryInterface
from src.models.dto.favourites import (FavouriteCategoryRequest, FavouriteCategoryResponse,
                                                FavouriteCategoryDTO, AllFavouriteCategoriesRequest)
from src.models.orm.category.favourite import FavouriteCategory


class FavouriteCategoryRepo(TablesRepositoryInterface):

    def __init__(self):
        self.model: FavouriteCategory = FavouriteCategory()

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def get_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryDTO:
        await session.scalars(
            select(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def drop_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...