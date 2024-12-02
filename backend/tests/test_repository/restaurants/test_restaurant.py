from sqlalchemy import text
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantRequestUsingID, Point, RestaurantGeoSearch, \
    RestaurantRequestUsingGeoPointAndName, RestaurantRequestUsingOwner
from src.repository.owner import OwnerRepo
from src.repository.restaurant.restaurant import RestaurantRepo
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager

from tests.common.restaurants import restaurants, get_search_result
from tests.sql_connector import get_session_test


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
        result = await RestaurantRepo(session_getter=get_session_test).create(model)
        assert expected_id == result.rest_id

async def test_create_multiple_rests(create_categories_and_owner, truncate_db):
    with does_not_raise():
        result1 = await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        result2 = await RestaurantRepo(session_getter=get_session_test).create(restaurants()[1])
        assert result1.rest_id == 1
        assert result2.rest_id == 2

async def test_delete_rest(create_categories_and_owner, truncate_db):
    with does_not_raise():
        inserted_id = await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        result = await RestaurantRepo(session_getter=get_session_test).delete(RestaurantRequestUsingID(rest_id=inserted_id.rest_id))
        assert result.rest_id == inserted_id.rest_id

async def test_update(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создать ресторан
        inserted_id = await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        # обновить его
        await RestaurantRepo(session_getter=get_session_test).update(inserted_id.rest_id, restaurants()[1])

async def test_get(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создать ресторан
        inserted_id = await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        rest = await RestaurantRepo(session_getter=get_session_test).get(RestaurantRequestUsingID(rest_id=inserted_id.rest_id))
        assert rest == restaurants()[0] # возвращенная схема должна быть равна той, что вставили

async def test_get_by_geo(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создали 3 ресторана
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        # получить список ресторанов
        rest_list = await RestaurantRepo(session_getter=get_session_test).get_by_geo(Point(lon=30, lat=60))
        assert rest_list == get_search_result()

async def test_get_by_geo_and_name(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создали 3 ресторана
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        # получить список ресторанов
        rest_list = await RestaurantRepo(session_getter=get_session_test).get_by_geo_and_name(
            RestaurantRequestUsingGeoPointAndName(point=Point(lon=30, lat=60), name_pattern='kf')
        )
        assert rest_list == get_search_result()

async def test_get_by_owner(create_categories_and_owner, truncate_db):
    with does_not_raise():
        # создали 3 ресторана
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[0])
        await RestaurantRepo(session_getter=get_session_test).create(restaurants()[1])

        # получить список всех рестиков у овнера 1
        rest_list = await RestaurantRepo(session_getter=get_session_test).get_by_owner(
            RestaurantRequestUsingOwner(owner_id=1)
        )
        assert rest_list == [restaurants()[0], restaurants()[1]]
