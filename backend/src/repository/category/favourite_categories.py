from typing import Optional

from sqlalchemy import select, insert, delete, Row
from src.models.dto.favourites import (FavouriteCategoryResponse, FavouriteCategoryDTO, AllFavouriteCategoriesRequest)
from src.models.orm.schemas import FavCatForUser
from src.repository.interface import TablesRepositoryInterface
from src.repository.user import UserRepo


class FavouriteCategoryRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        async with self.session_getter() as session:
            stmt = (
                delete(FavCatForUser)
                .where(FavCatForUser.user_id == model.user_id)
                .where(FavCatForUser.cat_id == model.cat_id)
            )
            await session.execute(stmt)
            return FavouriteCategoryResponse(cat_id=model.cat_id)

    async def create(
            self,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        async with self.session_getter() as session:
            # если юзера раньше не было в базе, то добавим
            user_repo = UserRepo(session_getter=self.session_getter)
            is_user = await user_repo.is_user(model.user_id)
            if not is_user:
                await user_repo.create_user(model.user_id)

            stmt = insert(FavCatForUser).values(**model.dict()).returning(FavCatForUser.cat_id)
            response = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = response.first()
            if row is None:
                raise ValueError("No category ID returned from the database")
            return FavouriteCategoryResponse(cat_id=int(row[0]))

    async def get_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> list[FavouriteCategoryResponse]:
        async with self.session_getter() as session:
            stmt = select(FavCatForUser.cat_id).where(FavCatForUser.user_id == model.user_id)
            fav_categories = await session.execute(stmt)
            return [
                FavouriteCategoryResponse.model_validate(cat, from_attributes=True) for cat in fav_categories.all()
            ]

    async def drop_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> AllFavouriteCategoriesRequest:
        async with self.session_getter() as session:
            stmt = select(FavCatForUser).where(FavCatForUser.user_id == model.user_id)
            await session.execute(stmt)
            return model