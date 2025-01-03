from typing import Optional

from sqlalchemy import select, insert, delete, Row, exists
from src.models.dto.favourites import (FavouriteRestaurantResponse, FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest)
from src.models.orm.schemas import FavRestForUser
from src.repository.interface import TablesRepositoryInterface
from src.repository.user import UserRepo


class FavouriteRestaurantRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: FavouriteRestaurantDTO
    ) -> FavouriteRestaurantResponse:
        async with self.session_getter() as session:
            stmt = (
                delete(FavRestForUser)
                .where(FavRestForUser.user_id == model.user_id)
                .where(FavRestForUser.rest_id == model.rest_id)
            )
            await session.execute(stmt)
            return FavouriteRestaurantResponse(rest_id=model.rest_id)

    async def create(
            self,
            model: FavouriteRestaurantDTO
    ) -> FavouriteRestaurantResponse:
        async with self.session_getter() as session:
            user_repo = UserRepo(session_getter=self.session_getter)
            is_user = await user_repo.is_user(model.user_id)
            if not is_user:
                await user_repo.create_user(model.user_id)
            stmt = insert(FavRestForUser).values(**model.dict()).returning(FavRestForUser.rest_id)
            response = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = response.first()
            if row is None:
                raise ValueError("No restaurant ID returned from the database")
            return FavouriteRestaurantResponse(rest_id=int(row[0]))

    async def get_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> list[FavouriteRestaurantResponse]:
        async with self.session_getter() as session:
            stmt = select(FavRestForUser.rest_id).where(FavRestForUser.user_id == model.user_id)
            fav_restaurants = await session.execute(stmt)
            return [
                FavouriteRestaurantResponse.model_validate(rest, from_attributes=True) for rest in fav_restaurants.all()
            ]

    async def drop_all_user_fav_restaurants(
            self,
            model: AllFavouriteRestaurantsRequest
    ) -> AllFavouriteRestaurantsRequest:
        async with self.session_getter() as session:
            stmt = delete(FavRestForUser).where(FavRestForUser.user_id == model.user_id)
            await session.execute(stmt)
            return model

    async def is_favourite(self, user_id: int, rest_id: int) -> bool:
        async with (self.session_getter() as session):

            # если юзера раньше не было в базе, то добавим
            user_repo = UserRepo(session_getter=self.session_getter)
            is_user = await user_repo.is_user(user_id)
            if not is_user:
                await user_repo.create_user(user_id)

            stmt = select(exists().where(
                FavRestForUser.user_id == user_id, FavRestForUser.rest_id == rest_id
            ))
            result = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = result.first()
            if row is None:
                raise ValueError("Nothing returned from the db")
            return row[0]
