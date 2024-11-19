from contextlib import _AsyncGeneratorContextManager
from typing import Callable, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from src.database.sql_session import get_session
from src.models.dto.restaurant import (RestaurantRequestUsingGeoPoint, RestaurantResponse,
                                                RestaurantResult, RestaurantRequestUsingOwner,
                                                RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                                RestaurantRequestFullModel)
from src.models.orm.schemas import Restaurant

class RestaurantRepo:

    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]] = get_session):
        """
        :session_getter Нужно передать коннектор к базе данных
        """
        self.session_getter = session_getter

    async def create(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        async with get_session() as session:
            stmt = insert(Restaurant).values(**model.dict()).returning(Restaurant.id)
            await session.execute(stmt)
            return RestaurantResult()

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        async with get_session() as session:
            stmt = delete(Restaurant).where(Restaurant.id == model.rest_id)
            await session.execute(stmt)
            return RestaurantResult()

    async def update(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        async with get_session() as session:
            stmt = update(Restaurant).where(Restaurant.id == model.id).values(**model.dict())
            await session.execute(stmt)
            return RestaurantResult()

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestFullModel:
        async with get_session() as session:
            stmt = select(
                Restaurant.owner_id, Restaurant.name,
                Restaurant.main_photo, Restaurant.photos,
                Restaurant.ext_serv_link_1, Restaurant.ext_serv_link_2, Restaurant.ext_serv_link_3,
                Restaurant.ext_serv_rank_1, Restaurant.ext_serv_rank_2, Restaurant.ext_serv_rank_3,
                Restaurant.ext_serv_reviews_1, Restaurant.ext_serv_reviews_2, Restaurant.ext_serv_reviews_3,
                Restaurant.tg_link, Restaurant.inst_link, Restaurant.vk_link,
                Restaurant.orig_phone, Restaurant.wapp_phone, Restaurant.location,
                Restaurant.address, Restaurant.categories
            ).where(Restaurant.id == model.rest_id)
            response = await session.execute(stmt)
            return RestaurantRequestFullModel.model_validate(response, from_attributes=True)

    async def get_by_geo(
            self,
            model: RestaurantRequestUsingGeoPoint
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            # todo: сделать тут поиск по гео
            return []

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            # todo: сделать тут поиск по гео
            return []

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            stmt = select(
                Restaurant.owner_id, Restaurant.name,
                Restaurant.main_photo, Restaurant.photos,
                Restaurant.ext_serv_link_1, Restaurant.ext_serv_link_2, Restaurant.ext_serv_link_3,
                Restaurant.ext_serv_rank_1, Restaurant.ext_serv_rank_2, Restaurant.ext_serv_rank_3,
                Restaurant.ext_serv_reviews_1, Restaurant.ext_serv_reviews_2, Restaurant.ext_serv_reviews_3,
                Restaurant.tg_link, Restaurant.inst_link, Restaurant.vk_link,
                Restaurant.orig_phone, Restaurant.wapp_phone, Restaurant.location,
                Restaurant.address, Restaurant.categories
            ).where(Restaurant.owner_id == model.owner_id)
            response = await session.execute(stmt)
            return [
                RestaurantRequestFullModel.model_validate(rest, from_attributes=True) for rest in response.all()
            ]