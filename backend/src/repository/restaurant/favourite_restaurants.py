from sqlalchemy import select, insert, delete, exists

from src.models.dto.favourites import FavouriteRestaurantDTO
from src.models.orm.schemas import FavRestForUser
from src.repository.interface import TablesRepositoryInterface
from src.repository.utils import create_user_if_does_not_exist, _execute_and_fetch_first


class FavouriteRestaurantRepo(TablesRepositoryInterface):

    async def delete(self, model: FavouriteRestaurantDTO) -> None:
        async with self.session_getter() as session:
            stmt = (
                delete(FavRestForUser)
                .where(FavRestForUser.user_id == model.user_id)
                .where(FavRestForUser.rest_id == model.rest_id)
            )
            await session.execute(stmt)

    async def create(self, model: FavouriteRestaurantDTO) -> int:
        async with self.session_getter() as session:
            await create_user_if_does_not_exist(session_getter=self.session_getter, user_id=model.user_id)
            stmt = insert(FavRestForUser).values(**model.model_dump()).returning(FavRestForUser.rest_id)
            row = await _execute_and_fetch_first(session, stmt, "No restaurant created")
            return int(row[0])

    async def get_all_user_fav_restaurants(
            self,
            user_id: int
    ) -> list[int]:
        async with self.session_getter() as session:
            stmt = select(FavRestForUser.rest_id).where(FavRestForUser.user_id == user_id)
            fav_restaurants = await session.execute(stmt)
            return [rest[0] for rest in fav_restaurants.all()]

    async def drop_all_user_fav_restaurants(
            self,
            user_id: int
    ) -> None:
        async with self.session_getter() as session:
            stmt = delete(FavRestForUser).where(FavRestForUser.user_id == user_id)
            await session.execute(stmt)

    async def is_favourite(self, user_id: int, rest_id: int) -> bool:
        async with (self.session_getter() as session):
            await create_user_if_does_not_exist(session_getter=self.session_getter, user_id=user_id)
            stmt = select(exists().where(
                FavRestForUser.user_id == user_id, FavRestForUser.rest_id == rest_id
            ))
            row = await _execute_and_fetch_first(session, stmt, "Something went wrong")
            return row[0]
