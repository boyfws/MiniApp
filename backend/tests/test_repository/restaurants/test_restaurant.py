from typing import Any, Optional

from sqlalchemy import text, Row
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantRequestUsingID, Point, RestaurantGeoSearch, \
    RestaurantRequestUsingGeoPointAndName, RestaurantRequestUsingOwner
from src.repository.owner import OwnerRepo
from src.repository.restaurant.restaurant import RestaurantRepo
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from tests.common.restaurants import restaurants, get_search_result
from tests.sql_connector import get_session_test

rest_repo = RestaurantRepo(session_getter=get_session_test)

@pytest.fixture(scope="function")
async def truncate_db():
    try:
        yield
    finally:
        async with get_session_test() as session_test:
            for table in [
                'owners', 'restaurants',
            ]:
                await session_test.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session_test.commit()

@pytest.fixture(scope='function')
async def create_categories_and_owner():
    await OwnerRepo(session_getter=get_session_test).create_owner(1)


@pytest.mark.parametrize(
    "model, expected_id, expectation",
    [(restaurants()[0], 1, does_not_raise()), (restaurants()[1], 1, does_not_raise())]
)
async def test_create_one_rest(
        model: RestaurantRequestFullModel,
        expected_id: int,
        expectation: AbstractContextManager,
        create_categories_and_owner,
        truncate_db
):
    with expectation:
        result = await rest_repo.create(model)
        assert expected_id == result.rest_id

async def test_create_multiple_rests(create_categories_and_owner, truncate_db):
    with does_not_raise():
        result1 = await rest_repo.create(restaurants()[0])
        result2 = await rest_repo.create(restaurants()[1])
        assert result1.rest_id == 1
        assert result2.rest_id == 2

async def test_delete_rest(create_categories_and_owner, truncate_db):
    with does_not_raise():
        inserted_id = await rest_repo.create(restaurants()[0])
        result = await rest_repo.delete(RestaurantRequestUsingID(rest_id=inserted_id.rest_id, user_id=1))
        assert result.rest_id == inserted_id.rest_id

async def test_update(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создать ресторан
        inserted_id = await rest_repo.create(restaurants()[0])
        # обновить его
        await rest_repo.update(inserted_id.rest_id, restaurants()[1])

async def test_get(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создать ресторан
        inserted_id = await rest_repo.create(restaurants()[0])
        rest = await rest_repo.get(RestaurantRequestUsingID(rest_id=inserted_id.rest_id, user_id=1))
        expected = restaurants()[0].model_dump()
        expected["favourite_flag"] = False
        assert rest.model_dump() == expected # возвращенная схема должна быть равна той, что вставили

async def test_get_by_geo(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создали 3 ресторана
        await rest_repo.create(restaurants()[0])
        await rest_repo.create(restaurants()[0])
        await rest_repo.create(restaurants()[0])
        # получить список ресторанов 125.6, 10.1
        rest_list = await rest_repo.get_by_geo(model=Point(lon=125.6, lat=10.1), user_id=1)
        assert rest_list == get_search_result()

async def test_get_by_geo_and_name(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создали 3 ресторана
        await rest_repo.create(restaurants()[0])
        await rest_repo.create(restaurants()[0])
        await rest_repo.create(restaurants()[0])
        # получить список ресторанов
        rest_list = await RestaurantRepo(session_getter=get_session_test).get_by_geo_and_name(
            model=RestaurantRequestUsingGeoPointAndName(point=Point(lon=125.6, lat=10.1), name_pattern='kf'),
            user_id=1
        )
        assert rest_list == get_search_result()

# async def test_get_by_owner(create_categories_and_owner, truncate_db):
#     with does_not_raise():
#         # создали 3 ресторана
#         await rest_repo.create(restaurants()[0])
#         await rest_repo.create(restaurants()[1])
#
#         # получить список всех рестиков у овнера 1
#         rest_list = await RestaurantRepo(session_getter=get_session_test).get_by_owner(
#             RestaurantRequestUsingOwner(owner_id=1)
#         )
#         expected_1, expected_2 = restaurants()[0].model_dump(), restaurants()[1].model_dump()
#         expected_1['favourite_flag'] = True
#         expected_2['favourite_flag'] = True
#         assert [rest_list[0].model_dump(), rest_list[1].model_dump()] == [expected_1, expected_2]

async def test_get_name(create_categories_and_owner, truncate_db):
    rest_id = await rest_repo.create(restaurants()[0])
    rest_name = await rest_repo.get_name(rest_id.rest_id)
    assert rest_name == 'kfc'

# @pytest.mark.parametrize(
#     "key, value",
#     [
#         ('name', 'КОТИК КОМАРУ'),
#         ('photos', ["pic.jpg", "citty.jpg", "cat.jpg", "dog.jpg"]),
#         ('location', 'SRID=4326;POINT(125.6 10.1)'),
#         ('address', {"type": "Feature", "geometry": {"type": "Point", "coordinates": [90.6, 10.1]}, "properties": {"name": "Moscow"}})
#     ]
# )
# async def test_change_property(key: str, value: Any, create_categories_and_owner, truncate_db):
#     rest_id = await rest_repo.create(restaurants()[0])
#     await rest_repo.change_restaurant_property(rest_id.rest_id, key, value)
#     async with get_session_test() as session:
#         # получить измененное проперти
#         if key != "location":
#             stmt = (
#                 f"SELECT {key} FROM restaurants WHERE id = {rest_id.rest_id};"
#             )
#         else:
#             stmt = (
#                 f"SELECT ST_AsEWKT(location) AS location FROM restaurants WHERE id = {rest_id.rest_id};"
#             )
#         result = await session.execute(text(stmt))
#         row: Optional[Row[tuple[str]]] = result.first()
#         if not row:
#             raise ValueError('no name returned')
#         actual_value = row[0]
#         assert actual_value == value