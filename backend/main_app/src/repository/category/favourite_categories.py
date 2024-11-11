from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.repository.interface import TablesRepositoryInterface
from src.models.dto.favourites import (FavouriteCategoryResponse, FavouriteCategoryDTO, AllFavouriteCategoriesRequest)
from src.models.orm.schemas import FavCatForUser


class FavouriteCategoryRepo:

    def __init__(self) -> None:
        self.model: FavCatForUser = FavCatForUser()

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        stmt = (
            delete(FavCatForUser)
            .where(FavCatForUser.user_id == model.user_id)
            .where(FavCatForUser.cat_id == model.cat_id)
        )
        await session.execute(stmt)
        return FavouriteCategoryResponse(cat_id=model.cat_id)

    async def create(
            self,
            session: AsyncSession,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        stmt = insert(FavCatForUser).values(**model.dict()).returning(FavCatForUser.cat_id)
        response = await session.execute(stmt)
        return FavouriteCategoryResponse.model_validate(response, from_attributes=True)

    async def get_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> list[FavouriteCategoryResponse]:
        stmt = select(FavCatForUser.cat_id).where(FavCatForUser.user_id == model.user_id)
        fav_categories = await session.execute(stmt)
        return [
            FavouriteCategoryResponse.model_validate(cat, from_attributes=True) for cat in fav_categories.all()
        ]

    async def drop_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        stmt = select(FavCatForUser).where(FavCatForUser.user_id == model.user_id)
        await session.execute(stmt)
        return FavouriteCategoryResponse(cat_id=model.user_id) # TODO: переделать здесь на другое возвращаемое значение