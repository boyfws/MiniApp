from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.dto.favourites import (FavouriteRestaurantResponse, FavouriteRestaurantDTO, AllFavouriteRestaurantsRequest)
from src.models.orm.schemas import FavRestForUser


class FavouriteRestaurantRepo:

    def __init__(self) -> None:
        self.model: FavRestForUser = FavRestForUser()

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantDTO
    ) -> FavouriteRestaurantResponse:
        stmt = (
            delete(FavRestForUser)
            .where(FavRestForUser.user_id == model.user_id)
            .where(FavRestForUser.rest_id == model.rest_id)
        )
        await session.execute(stmt)
        return FavouriteRestaurantResponse(rest_id=model.rest_id)

    async def create(
            self,
            session: AsyncSession,
            model: FavouriteRestaurantDTO
    ) -> FavouriteRestaurantResponse:
        stmt = insert(FavRestForUser).values(**model.dict()).returning(FavRestForUser.rest_id)
        response = await session.execute(stmt)
        return FavouriteRestaurantResponse.model_validate(response, from_attributes=True)

    async def get_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> list[FavouriteRestaurantResponse]:
        stmt = select(FavRestForUser.rest_id).where(FavRestForUser.user_id == model.user_id)
        fav_restaurants = await session.execute(stmt)
        return [
            FavouriteRestaurantResponse.model_validate(rest, from_attributes=True) for rest in fav_restaurants.all()
        ]

    async def drop_all_user_fav_restaurants(
            self,
            session: AsyncSession,
            model: AllFavouriteRestaurantsRequest
    ) -> FavouriteRestaurantResponse:
        stmt = select(FavRestForUser).where(FavRestForUser.user_id == model.user_id)
        await session.execute(stmt)
        return FavouriteRestaurantResponse(rest_id=model.user_id)  # TODO: переделать здесь на другое возвращаемое значение