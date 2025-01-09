import json
from typing import Any

from asyncpg import Record # type: ignore
from geoalchemy2 import Geography
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint
from sqlalchemy import select, insert, delete, update, Row, text, func, cast

from src.models.dto.restaurant import (RestaurantResult, RestaurantRequestUsingOwner,
                                       RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                       RestaurantGeoSearch, Point, RestaurantDTO,
                                       RestaurantRequestUpdateModel, GeoSearchResult)
from src.models.orm.schemas import Restaurant
from src.repository.category.category import CategoryRepo
from src.repository.interface import TablesRepositoryInterface
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
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
    ) -> RestaurantResult:
        async with self.session_getter() as session:
            await create_owner_if_does_not_exist(self.session_getter, model.owner_id)
            stmt = insert(Restaurant).values(**model.model_dump()).returning(Restaurant.id)
            row = await _execute_and_fetch_first(session, stmt, "Something went wrong")
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
            stmt = select(
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
            ).where(Restaurant.id == model.rest_id)
            row = await _execute_and_fetch_first(session, stmt, "No restaurant with such id")
            rest_model = dict(zip(names, row))
            return RestaurantRequestUpdateModel.model_validate(rest_model, from_attributes=True)

    async def get_by_geo(
            self,
            model: Point
    ) -> list[GeoSearchResult]:
        async with self.session_getter() as session:
            point = ST_SetSRID(ST_MakePoint(model.lon, model.lat), 4326)
            distance = func.ST_Distance(Restaurant.location, cast(point, Geography)).label("distance")
            stmt = (
                select(
                    Restaurant.id, Restaurant.name, Restaurant.main_photo,
                    Restaurant.categories, Restaurant.ext_serv_rank_1, distance,
                )
                .where(func.ST_DWithin(Restaurant.location, cast(point, Geography), 15000))
                .order_by(distance)
                .limit(100)
            )
            result = await session.execute(stmt)
            rest_tuple: Record = result.fetchall()
            return [
                GeoSearchResult.model_validate(
                    dict(zip(names_search, rest)),
                    from_attributes=True
                ) for rest in rest_tuple
            ]

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            point = ST_SetSRID(ST_MakePoint(model.point.lon, model.point.lat), 4326)
            distance = func.ST_Distance(Restaurant.location, cast(point, Geography)).label("distance")
            stmt = (
                select(
                    Restaurant.id, Restaurant.name, Restaurant.main_photo,
                    Restaurant.categories, Restaurant.ext_serv_rank_1, distance,
                )
                .where(func.ST_DWithin(Restaurant.location, cast(point, Geography), 15000))
                .where(text(f"name % '{model.name_pattern}'"))
                .order_by(distance)
                .limit(100)
            )
            result = await session.execute(stmt)
            rest_tuple: Record = result.fetchall()
            return [
                GeoSearchResult.model_validate(
                    dict(zip(names_search, rest)),
                    from_attributes=True
                ) for rest in rest_tuple
            ]


    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantDTO]:
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

            cat_repo = CategoryRepo(session_getter=self.session_getter)

            transformed_data = []
            for rest in rest_tuple:
                rest_dict = {}
                for col in rest._fields:
                    value = getattr(rest, col)
                    if col == 'categories':
                        rest_dict[col] = [await cat_repo.get_name(cat) for cat in value]
                    elif col == 'photos':
                        rest_dict[col] = value if value else []
                    elif col == 'address':
                        try:
                            rest_dict[col] = json.loads(value)
                        except (json.JSONDecodeError, TypeError):
                            rest_dict[col] = {}
                    elif col == 'location':
                        rest_dict[col] = str(value) if value else None  # handle NULL locations
                    else:
                        rest_dict[col] = value
                rest_dict['favourite_flag'] = True
                transformed_data.append(RestaurantDTO(**rest_dict))
            return transformed_data

    async def get_name(self, rest_id: int) -> str:
        async with self.session_getter() as session:
            stmt = select(Restaurant.name).where(Restaurant.id == rest_id)
            row = await _execute_and_fetch_first(session, stmt, "No restaurant with such id")
            return row[0]

    async def change_restaurant_property(self, rest_id: int, key: str, value: Any) -> None:
        async with self.session_getter() as session:
            if key == "location":
                stmt = (
                    "UPDATE restaurants "
                    f"SET {key} = {value} "
                    f"WHERE id = {rest_id};"
                )
                await session.execute(text(stmt))
            if isinstance(value, list):
                stmt = (
                    "UPDATE restaurants "
                    f'SET {key} = ARRAY{value} '
                    f"WHERE id = {rest_id};"
                )
            elif isinstance(value, str):
                stmt = (
                    "UPDATE restaurants "
                    f"SET {key} = '{value}' "
                    f"WHERE id = {rest_id};"
                )
            elif isinstance(value, dict):
                ddd = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [34, 34]
                    },
                    "properties": {
                        "city": "Saint Petersburg",
                        "street": "Nevsky Prospect",
                        "house": "28",
                    }
                }
                stmt = (
                    "UPDATE restaurants "
                    f'SET {key} = {ddd}::JSONB '
                    f"WHERE id = {rest_id};"
                )
            else:
                raise ValueError("введите правильный тип (str, dict, list)")
            await session.execute(text(stmt))