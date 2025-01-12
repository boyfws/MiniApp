from sqlalchemy import select, delete

from src.models.dto.favourites import FavouriteCategoryRequest
from src.models.orm.schemas import FavCatForUser
from src.repository.category import add_fav_cat_for_user, extract_name_by_id_for_all_categories
from src.repository.interface import TablesRepositoryInterface


class FavouriteCategoryRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: FavouriteCategoryRequest
    ) -> None:
        async with self.session_getter() as session:
            stmt = (
                delete(FavCatForUser)
                .where(FavCatForUser.user_id == model.user_id)
                .where(FavCatForUser.cat_id == model.cat_id)
            )
            await session.execute(stmt)

    async def create(
            self,
            model: FavouriteCategoryRequest
    ) -> None:
        async with self.session_getter() as session:
            await add_fav_cat_for_user(session=session, cat_id=model.cat_id, user_id=model.user_id)

    async def get_all_user_fav_categories(
            self,
            user_id: int
    ) -> list[int]:
        async with self.session_getter() as session:
            stmt = select(FavCatForUser.cat_id).where(FavCatForUser.user_id == user_id)
            fav_categories = await session.execute(stmt)
            return [cat[0] for cat in fav_categories.all()]

    async def drop_all_user_fav_categories(self, user_id: int) -> None:
        async with self.session_getter() as session:
            stmt = delete(FavCatForUser).where(FavCatForUser.user_id == user_id)
            await session.execute(stmt)