import asyncio
import json
from typing import Optional, Any

from asyncpg import Record # type: ignore
from sqlalchemy import select, insert, delete, update, Row, text

from src.models.dto.category import CategoryDTO
from src.models.dto.restaurant import (RestaurantResult, RestaurantRequestUsingOwner,
                                       RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                       RestaurantRequestFullModel, RestaurantGeoSearch, Point, RestaurantDTO,
                                       RestaurantRequestUpdateModel)
from src.models.orm.schemas import Restaurant
from src.repository.category.category import CategoryRepo
from src.repository.interface import TablesRepositoryInterface
from src.repository.owner import OwnerRepo
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.utils import _execute_and_fetch_first, create_owner_if_does_not_exist

names = ['owner_id', 'name', 'main_photo', 'photos',
         'ext_serv_link_1', 'ext_serv_link_2', 'ext_serv_link_3',
         'ext_serv_rank_1', 'ext_serv_rank_2', 'ext_serv_rank_3',
         'ext_serv_reviews_1', 'ext_serv_reviews_2', 'ext_serv_reviews_3',
         'tg_link', 'inst_link', 'vk_link', 'orig_phone', 'wapp_phone',
         'location', 'address', 'categories']

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
            model: RestaurantRequestFullModel
    ) -> None:
        async with self.session_getter() as session:
            cat_repo = CategoryRepo(session_getter=self.session_getter)
            category_list = [(await cat_repo.get(CategoryDTO(name=name))).cat_id for name in model.categories]

            model_copy = model.model_dump()

            model_copy['categories'] = category_list
            stmt = update(Restaurant).where(Restaurant.id == rest_id).values(**model_copy)
            await session.execute(stmt)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantDTO:
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

            cat_repo = CategoryRepo(session_getter=self.session_getter)
            fav_rest_repo = FavouriteRestaurantRepo(session_getter=self.session_getter)

            rest_model['favourite_flag'] = await fav_rest_repo.is_favourite(model.rest_id, model.user_id)
            rest_model['categories'] = [await cat_repo.get_name(int(num)) for num in rest_model['categories']]
            return RestaurantDTO(**rest_model)

    async def get_by_geo(
            self,
            user_id: int,
            model: Point
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            query = (
                "SELECT "
                    "id, name, main_photo, categories, ext_serv_rank_1, "
                    "ST_Distance("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.lon}, {model.lat}), 4326)::geography"
                    ") AS distance "
                "FROM restaurants "
                "WHERE "
                    "ST_DWithin("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.lon}, {model.lat}), 4326)::geography, "
                        "15000 " # расстояние в метрах
                    ") "
                "ORDER BY distance "
                "LIMIT 100;"
            )
            result = await session.execute(text(query))
            rest_tuple: Record = result.fetchall()
            if not rest_tuple:
                return []

            cat_repo = CategoryRepo(session_getter=self.session_getter)
            fav_rest_repo = FavouriteRestaurantRepo(session_getter=self.session_getter)

            async def transform_row(row):
                return {
                    "id": row.id,
                    "name": row.name,
                    "main_photo": row.main_photo,
                    "distance": round(row.distance / 1000, 2),
                    'favourite_flag': await fav_rest_repo.is_favourite(user_id=user_id, rest_id=row.id),
                    "category": [await cat_repo.get_name(cat_id=int(cat)) for cat in row.categories],
                    'rating': row.ext_serv_rank_1 if row.ext_serv_rank_1 else 0
                }

            transformed_data = [await transform_row(rest) for rest in rest_tuple]
            return [RestaurantGeoSearch.model_validate(data, from_attributes=True) for data in transformed_data]

    async def get_by_geo_and_name(
            self,
            user_id: int,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        async with self.session_getter() as session:
            query = (
                "SELECT "
                    "id, name, main_photo, categories, ext_serv_rank_1, "
                    "ST_Distance("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.point.lon}, {model.point.lat}), 4326)::geography"
                    ") AS distance "
                "FROM restaurants "
                "WHERE "
                    "ST_DWithin("
                        "location, "
                        f"ST_SetSRID(ST_MakePoint({model.point.lon}, {model.point.lat}), 4326)::geography, "
                        "15000 "  # расстояние в метрах
                    ") "
                "AND "
                    f"name % '{model.name_pattern}'"
                "ORDER BY distance "
                "LIMIT 100;"
            )
            result = await session.execute(text(query))
            rest_tuple: Record = result.fetchall()
            if not rest_tuple:
                return []

            cat_repo = CategoryRepo(session_getter=self.session_getter)
            fav_rest_repo = FavouriteRestaurantRepo(session_getter=self.session_getter)

            async def transform_row(row):
                return {
                    "id": row.id,
                    "name": row.name,
                    "main_photo": row.main_photo,
                    "distance": round(row.distance / 1000, 2),
                    'favourite_flag': await fav_rest_repo.is_favourite(row.id, user_id),
                    "category": [await cat_repo.get_name(cat_id=int(cat)) for cat in row.categories],
                    'rating': row.ext_serv_rank_1 if row.ext_serv_rank_1 else 0
                }

            transformed_data = [await transform_row(rest) for rest in rest_tuple]
            return [RestaurantGeoSearch.model_validate(data, from_attributes=True) for data in transformed_data]


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