from typing import Optional

from asyncpg import Record # type: ignore
from sqlalchemy import select, insert, delete, update, Row, text
from src.models.dto.restaurant import (RestaurantResult, RestaurantRequestUsingOwner,
                                       RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                       RestaurantRequestFullModel, RestaurantGeoSearch, Point)
from src.models.orm.schemas import Restaurant
from src.repository.interface import TablesRepositoryInterface

names = ['owner_id', 'name', 'main_photo', 'photos',
         'ext_serv_link_1', 'ext_serv_link_2', 'ext_serv_link_3',
         'ext_serv_rank_1', 'ext_serv_rank_2', 'ext_serv_rank_3',
         'ext_serv_reviews_1', 'ext_serv_reviews_2', 'ext_serv_reviews_3',
         'tg_link', 'inst_link', 'vk_link', 'orig_phone', 'wapp_phone',
         'location', 'address', 'categories']

class RestaurantRepo(TablesRepositoryInterface):

    async def create(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        async with self.session_getter() as session:
            stmt = insert(Restaurant).values(**model.model_dump()).returning(Restaurant.id)
            result = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = result.first()
            if not row:
                raise ValueError('no id returned')
            return RestaurantResult(rest_id=int(row[0]))

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        async with self.session_getter() as session:
            stmt = delete(Restaurant).where(Restaurant.id == model.rest_id)
            await session.execute(stmt)
            return RestaurantResult(rest_id=model.rest_id)

    async def update(
            self,
            rest_id: int,
            model: RestaurantRequestFullModel
    ) -> None:
        async with self.session_getter() as session:
            stmt = update(Restaurant).where(Restaurant.id == rest_id).values(**model.model_dump())
            await session.execute(stmt)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestFullModel:
        async with self.session_getter() as session:
            query = (
                 "SELECT "
                 "owner_id, name, main_photo, photos, "
                 "ext_serv_link_1, ext_serv_link_2, ext_serv_link_3,"
                 "ext_serv_rank_1, ext_serv_rank_2, ext_serv_rank_3,"
                 "ext_serv_reviews_1, ext_serv_reviews_2, ext_serv_reviews_3,"
                 "tg_link, inst_link, vk_link, orig_phone, wapp_phone, "
                 "ST_AsEWKT(location) AS location, "
                 "address, categories "
                 f"FROM restaurants WHERE id = {model.rest_id}"
            )
            response = await session.execute(text(query))
            rest_tuple: Record = response.first()
            if not rest_tuple:
                raise ValueError(f"no restaurant with id {model.rest_id}")
            rest_model = dict(zip(names, rest_tuple))
            return RestaurantRequestFullModel(**rest_model)

    async def get_by_geo(
            self,
            model: Point
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            query = (
                "SELECT "
                    "id, name, main_photo, "
                    "ST_Distance("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.lon}, {model.lat}), 4326)::geography"
                    ") AS distance "
                "FROM restaurants "
                "WHERE "
                    "ST_DWithin("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.lon}, {model.lat}), 4326)::geography, "
                        "10000000000000 " # расстояние в метрах
                    ") "
                "ORDER BY distance "
                "LIMIT 10;"
            )
            result = await session.execute(text(query))
            rest_tuple: Record = result.fetchall()
            if not rest_tuple:
                return []
            return [RestaurantGeoSearch.model_validate(rest, from_attributes=True) for rest in rest_tuple]

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            query = (
                "SELECT "
                    "id, name, main_photo, "
                    "ST_Distance("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.point.lon}, {model.point.lat}), 4326)::geography"
                    ") AS distance "
                "FROM restaurants "
                "WHERE "
                    "ST_DWithin("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.point.lon}, {model.point.lat}), 4326)::geography, "
                        "10000000000000 "  # расстояние в метрах
                    ") "
                "AND "
                    f"name LIKE '{model.name_pattern}%'"
                "ORDER BY distance "
                "LIMIT 10;"
            )
            result = await session.execute(text(query))
            rest_tuple: Record = result.fetchall()
            if not rest_tuple:
                return []
            return [RestaurantGeoSearch.model_validate(rest, from_attributes=True) for rest in rest_tuple]


    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
        async with self.session_getter() as session:
            query = (
                "SELECT "
                "owner_id, name, main_photo, photos, "
                "ext_serv_link_1, ext_serv_link_2, ext_serv_link_3,"
                "ext_serv_rank_1, ext_serv_rank_2, ext_serv_rank_3,"
                "ext_serv_reviews_1, ext_serv_reviews_2, ext_serv_reviews_3,"
                "tg_link, inst_link, vk_link, orig_phone, wapp_phone, "
                "ST_AsEWKT(location) AS location, "
                "address, categories "
                f"FROM restaurants WHERE owner_id = {model.owner_id}"
            )
            response = await session.execute(text(query))
            rest_tuple: Record = response.fetchall()
            if not rest_tuple:
                return []
            return [
                RestaurantRequestFullModel.model_validate(rest, from_attributes=True) for rest in rest_tuple
            ]