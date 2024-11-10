from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.repository.interface import TablesRepositoryInterface
from src.models.dto.favourites import (FavouriteCategoryRequest, FavouriteCategoryResponse,
                                                FavouriteCategoryDTO, AllFavouriteCategoriesRequest)
from src.models.orm.schemas import FavCatForUser


class FavouriteCategoryRepo:

    def __init__(self) -> None:
        self.model: FavCatForUser = FavCatForUser()

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        return FavouriteCategoryResponse()

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        return FavouriteCategoryResponse()

    async def get(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryDTO:
        return FavouriteCategoryDTO()

    async def get_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryDTO:
        return FavouriteCategoryDTO()

    async def drop_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        return FavouriteCategoryResponse()