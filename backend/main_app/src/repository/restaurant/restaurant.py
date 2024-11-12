from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from src.models.dto.restaurant import (RestaurantRequestUsingGeoPoint, RestaurantResponse,
                                                RestaurantResult, RestaurantRequestUsingOwner,
                                                RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                                RestaurantRequestFullModel)
from src.models.orm.schemas import Restaurant

class RestaurantRepo:

    async def create(
            self,
            session: AsyncSession,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        stmt = insert(Restaurant).values(**model.dict()).returning(Restaurant.id)
        await session.execute(stmt)
        return RestaurantResult()

    async def delete(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        stmt = delete(Restaurant).where(Restaurant.id == model.rest_id)
        await session.execute(stmt)
        return RestaurantResult()

    async def update(
            self,
            session: AsyncSession,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        stmt = update(Restaurant).where(Restaurant.id == model.id).values(**model.dict())
        await session.execute(stmt)
        return RestaurantResult()

    async def get(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestFullModel:
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
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPoint
    ) -> list[RestaurantRequestFullModel]:
        # todo: сделать тут поиск по гео
        return []

    async def get_by_geo_and_name(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantRequestFullModel]:
        # todo: сделать тут поиск по гео
        return []

    async def get_by_owner(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
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


