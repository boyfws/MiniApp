from sqlalchemy import select, delete

from src.models.dto.favourites import FavouriteCategoryDTO
from src.models.orm.schemas import FavCatForUser
from src.repository.category import add_fav_cat_for_user, extract_name_by_id_for_all_categories
from src.repository.category.category import CategoryRepo
from src.repository.interface import TablesRepositoryInterface
from src.repository.utils import create_user_if_does_not_exist


class FavouriteCategoryRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: FavouriteCategoryDTO
    ) -> None:
        async with self.session_getter() as session:
            # получим айди категории по названию
            cat_repo = CategoryRepo(session_getter=self.session_getter)
            cat_id = await cat_repo.get(cat_name=model.cat_name) # TODO: протечка слоев!!!!!!!!!!!!!

            # удалим категорию из любимых по айди
            stmt = (
                delete(FavCatForUser)
                .where(FavCatForUser.user_id == model.user_id)
                .where(FavCatForUser.cat_id == cat_id)
            )
            await session.execute(stmt)

    async def create(
            self,
            model: FavouriteCategoryDTO
    ) -> None:
        async with self.session_getter() as session:
            await create_user_if_does_not_exist(session_getter=self.session_getter, user_id=model.user_id)
            # получим айди категории по названию
            cat_repo = CategoryRepo(session_getter=self.session_getter) # TODO: протечка слоев!!!!!!!!!
            cat_id = await cat_repo.get(cat_name=model.cat_name)
            await add_fav_cat_for_user(session=session, cat_id=cat_id, user_id=model.user_id)

    async def get_all_user_fav_categories(
            self,
            user_id: int
    ) -> list[str]:
        async with self.session_getter() as session:
            stmt = select(FavCatForUser.cat_id).where(FavCatForUser.user_id == user_id)
            fav_categories = await session.execute(stmt)
            # TODO: протечка слоев!!!!!!!!!!!!
            transformed = await extract_name_by_id_for_all_categories(self.session_getter, fav_categories)
            return [cat['cat_name'] for cat in transformed]

    async def drop_all_user_fav_categories(self, user_id: int) -> None:
        async with self.session_getter() as session:
            stmt = delete(FavCatForUser).where(FavCatForUser.user_id == user_id)
            await session.execute(stmt)