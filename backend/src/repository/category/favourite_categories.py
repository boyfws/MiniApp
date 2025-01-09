from typing import Optional

from sqlalchemy import select, insert, delete, Row

from src.models.dto.category import CategoryDTO
from src.models.dto.favourites import (FavouriteCategoryResponse, FavouriteCategoryDTO, AllFavouriteCategoriesRequest)
from src.models.orm.schemas import FavCatForUser
from src.repository.category import add_fav_cat_for_user, extract_name_by_id_for_all_categories
from src.repository.category.category import CategoryRepo
from src.repository.interface import TablesRepositoryInterface
from src.repository.user import UserRepo
from src.repository.utils import create_user_if_does_not_exist


class FavouriteCategoryRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        async with self.session_getter() as session:
            # получим айди категории по названию
            cat_repo = CategoryRepo(session_getter=self.session_getter)
            cat_id = await cat_repo.get(CategoryDTO(name=model.cat_name))

            # удалим категорию из любимых по айди
            stmt = (
                delete(FavCatForUser)
                .where(FavCatForUser.user_id == model.user_id)
                .where(FavCatForUser.cat_id == cat_id.cat_id)
            )
            await session.execute(stmt)
            return FavouriteCategoryResponse(cat_name=model.cat_name)

    async def create(
            self,
            model: FavouriteCategoryDTO
    ) -> FavouriteCategoryResponse:
        async with self.session_getter() as session:
            await create_user_if_does_not_exist(session_getter=self.session_getter, user_id=model.user_id)
            # получим айди категории по названию
            cat_repo = CategoryRepo(session_getter=self.session_getter)
            cat_id = await cat_repo.get(CategoryDTO(name=model.cat_name))
            await add_fav_cat_for_user(session=session, cat_id=cat_id.cat_id, user_id=model.user_id)
            return FavouriteCategoryResponse(cat_name=model.cat_name)

    async def get_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> list[FavouriteCategoryResponse]:
        async with self.session_getter() as session:
            stmt = select(FavCatForUser.cat_id).where(FavCatForUser.user_id == model.user_id)
            fav_categories = await session.execute(stmt)
            transformed = await extract_name_by_id_for_all_categories(self.session_getter, fav_categories)
            return [
                FavouriteCategoryResponse.model_validate(cat, from_attributes=True) for cat in transformed
            ]

    async def drop_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> AllFavouriteCategoriesRequest:
        async with self.session_getter() as session:
            stmt = delete(FavCatForUser).where(FavCatForUser.user_id == model.user_id)
            await session.execute(stmt)
            return model