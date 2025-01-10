from typing import Any, Sequence

from asyncpg import Record # type: ignore
from geoalchemy2 import Geography
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint
from sqlalchemy import select, insert, delete, update, Row, text, func, cast, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dto.restaurant import (RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                       RestaurantGeoSearch, Point,
                                       RestaurantRequestUpdateModel, GeoSearchResult)
from src.models.orm.schemas import Restaurant
from src.repository.interface import TablesRepositoryInterface
from src.repository.utils import _execute_and_fetch_first, create_owner_if_does_not_exist

names = ['owner_id', 'name', 'main_photo', 'photos',
         'ext_serv_link_1', 'ext_serv_link_2', 'ext_serv_link_3',
         'ext_serv_rank_1', 'ext_serv_rank_2', 'ext_serv_rank_3',
         'ext_serv_reviews_1', 'ext_serv_reviews_2', 'ext_serv_reviews_3',
         'tg_link', 'inst_link', 'vk_link', 'orig_phone', 'wapp_phone',
         'location', 'address', 'categories']

names_search = [
    'id', 'name', 'main_photo', 'category', 'rating', 'distance'
]

class RestaurantRepo(TablesRepositoryInterface):

    async def create(
            self,
            model: RestaurantRequestUpdateModel
    ) -> int:
        async with self.session_getter() as session:
            await create_owner_if_does_not_exist(self.session_getter, model.owner_id)
            stmt = insert(Restaurant).values(**model.model_dump()).returning(Restaurant.id)
            row = await _execute_and_fetch_first(session, stmt, "Something went wrong")
            return int(row[0])

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> None:
        async with self.session_getter() as session:
            stmt = delete(Restaurant).where(Restaurant.id == model.rest_id)
            await session.execute(stmt)

    async def update(
            self,
            rest_id: int,
            model: RestaurantRequestUpdateModel
    ) -> None:
        async with self.session_getter() as session:
            stmt = update(Restaurant).where(Restaurant.id == rest_id).values(**model.model_dump())
            await session.execute(stmt)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestUpdateModel:
        async with self.session_getter() as session:
            return RestaurantRequestUpdateModel.model_validate(
                await self._execute_get(session, model),
                from_attributes=True
            )

    async def get_by_geo(
            self,
            model: Point
    ) -> list[GeoSearchResult]:
        async with self.session_getter() as session:
            return [
                GeoSearchResult.model_validate(
                    dict(zip(names_search, rest)),
                    from_attributes=True
                ) for rest in await self._execute_select_stmt(session, self._get_search_stmt(model))
            ]

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            return [
                GeoSearchResult.model_validate(
                    dict(zip(names_search, rest)),
                    from_attributes=True
                ) for rest in await self._execute_select_stmt(session, self._get_text_search_stmt(model))
            ]


    async def get_by_owner(
            self,
            owner_id: int
    ) -> list[RestaurantRequestUpdateModel]:
        async with self.session_getter() as session:
            return [
                RestaurantRequestUpdateModel.model_validate(
                    rest,
                    from_attributes=True
                ) for rest in await self._execute_select_stmt(session, self._get_by_owner_stmt(owner_id))
            ]

    async def get_name(self, rest_id: int) -> str:
        async with self.session_getter() as session:
            stmt = select(Restaurant.name).where(Restaurant.id == rest_id)
            row = await _execute_and_fetch_first(session, stmt, "No restaurant with such id")
            return row[0]

    async def change_restaurant_property(self, rest_id: int, key: str, value: Any) -> None:
        async with self.session_getter() as session:
            await self._execute_update(rest_id, key, value, session)

    @staticmethod
    async def _execute_update(rest_id: int, key: str, value: Any, session: AsyncSession) -> None:
        stmt = update(Restaurant).where(Restaurant.id == rest_id).values(**{key: value})
        await session.execute(stmt)

    @staticmethod
    def _get_search_stmt(model) -> Select:
        point = ST_SetSRID(ST_MakePoint(model.lon, model.lat), 4326)
        distance = func.ST_Distance(Restaurant.location, cast(point, Geography)).label("distance")
        return (
            select(
                Restaurant.id, Restaurant.name, Restaurant.main_photo,
                Restaurant.categories, Restaurant.ext_serv_rank_1, distance,
            )
            .where(func.ST_DWithin(Restaurant.location, cast(point, Geography), 15000))
            .order_by(distance)
            .limit(100)
        )

    @staticmethod
    def _get_text_search_stmt(model) -> Select:
        point = ST_SetSRID(ST_MakePoint(model.point.lon, model.point.lat), 4326)
        distance = func.ST_Distance(Restaurant.location, cast(point, Geography)).label("distance")
        return (
            select(
                Restaurant.id, Restaurant.name, Restaurant.main_photo,
                Restaurant.categories, Restaurant.ext_serv_rank_1, distance,
            )
            .where(func.ST_DWithin(Restaurant.location, cast(point, Geography), 15000))
            .where(text(f"name % '{model.name_pattern}'"))
            .order_by(distance)
            .limit(100)
        )

    @staticmethod
    async def _execute_select_stmt(session: AsyncSession, stmt: Select) -> Sequence[Row]:
        response = await session.execute(stmt)
        return response.fetchall()

    @staticmethod
    def _get_all_fields() -> Select:
        return select(
            Restaurant.owner_id,
            Restaurant.name,
            Restaurant.main_photo,
            Restaurant.photos,
            Restaurant.ext_serv_link_1,
            Restaurant.ext_serv_link_2,
            Restaurant.ext_serv_link_3,
            Restaurant.ext_serv_rank_1,
            Restaurant.ext_serv_rank_2,
            Restaurant.ext_serv_rank_3,
            Restaurant.ext_serv_reviews_1,
            Restaurant.ext_serv_reviews_2,
            Restaurant.ext_serv_reviews_3,
            Restaurant.tg_link,
            Restaurant.inst_link,
            Restaurant.vk_link,
            Restaurant.orig_phone,
            Restaurant.wapp_phone,
            func.ST_AsEWKT(Restaurant.location).label("location"),
            Restaurant.address,
            Restaurant.categories,
        )

    def _get_base_get_stmt(self, model: RestaurantRequestUsingID) -> Select:
        return self._get_all_fields().where(Restaurant.id == model.rest_id)

    async def _execute_get(self, session: AsyncSession, model: RestaurantRequestUsingID) -> dict[str, Any]:
        row = await _execute_and_fetch_first(
            session,
            self._get_base_get_stmt(model),
            "No restaurant with such id"
        )
        return dict(zip(names, row))

    def _get_by_owner_stmt(self, owner_id: int) -> Select:
        return self._get_all_fields().where(Restaurant.owner_id == owner_id)