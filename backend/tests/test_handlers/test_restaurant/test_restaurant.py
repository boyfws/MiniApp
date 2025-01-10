from typing import Any

import pytest
from sqlalchemy import text

from src.models.dto.restaurant import RestaurantRequestFullModel
from tests.common.restaurants import restaurants, get_search_result
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.test_repository.test_restaurants.test_restaurants import create_categories_and_owner, truncate_db


@pytest.mark.parametrize(
    "model, expected_id",
    [(restaurants()[0], 1), (restaurants()[1], 1)]
)
async def test_create(
        model: RestaurantRequestFullModel,
        expected_id: int,
        test_app,
        create_categories_and_owner,
        truncate_db
):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=model.model_dump())
    assert response.status_code == 200
    assert response.json() == expected_id

async def test_delete(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()
    result = await test_app.delete(f'/v1_test/Restaurant/delete_restaurant/{inserted_id}/{1}')
    assert result.status_code == 200
    async with get_session_test() as session:
        count = await session.execute(text(f"SELECT COUNT(*) FROM restaurants WHERE id = {inserted_id}"))
        assert count.scalar() == 0

async def test_update(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()
    result = await test_app.patch(f'/v1_test/Restaurant/update_restaurant/{inserted_id}', json=restaurants()[0].model_dump())
    assert result.status_code == 200

async def test_get(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()
    result = await test_app.get(f"/v1_test/Restaurant/get_by_id/{inserted_id}/{1}")
    assert result.status_code == 200
    expected = restaurants()[0].model_dump()
    expected['favourite_flag'] = False
    assert result.json() == expected

async def test_get_by_geo(create_categories_and_owner, truncate_db, test_app):
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())

    rest_list_response = await test_app.get(f"/v1_test/Restaurant/get_by_geo/{125.6}/{10.1}/{1}")
    assert rest_list_response.status_code == 200
    assert rest_list_response.json() == [data.model_dump() for data in get_search_result()]

async def test_get_by_geo_and_name(create_categories_and_owner, truncate_db, test_app):
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())

    rest_list_response = await test_app.get(f"/v1_test/Restaurant/get_by_geo_and_name/{125.6}/{10.1}/{'kf'}/{1}")
    assert rest_list_response.status_code == 200
    assert rest_list_response.json() == [data.model_dump() for data in get_search_result()]

async def test_get_by_owner(create_categories_and_owner, truncate_db, test_app):
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[1].model_dump())

    rest_list = await test_app.get(f'/v1_test/Restaurant/get_by_owner/{1}')
    assert rest_list.status_code == 200
    assert rest_list.json() == [data.model_dump() for data in restaurants()[:2]]

async def test_get_name(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    rest_id = response.json()
    result = await test_app.get(f"/v1_test/Restaurant/get_restaurant_name_by_id/{rest_id}")
    assert result.status_code == 200
    assert result.json() == 'kfc'

async def test_get_properties(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    rest_id = response.json()
    result = await test_app.get(f"/v1_test/Restaurant/get_restaurant_available_properties/{rest_id}")
    assert result.status_code == 200
    assert result.json() == {
        'owner_id': True,
        'name': True,
        'main_photo': True,
        'photos': True,
        'ext_serv_link_1': False,
        'ext_serv_link_2': False,
        'ext_serv_link_3': False,
        'ext_serv_rank_1': False,
        'ext_serv_rank_2': False,
        'ext_serv_rank_3': False,
        'ext_serv_reviews_1': False,
        'ext_serv_reviews_2': False,
        'ext_serv_reviews_3': False,
        'tg_link': False,
        'inst_link': False,
        'vk_link': False,
        'orig_phone': True,
        'wapp_phone': True,
        'location': True,
        'address': True,
        'categories': True
    }

@pytest.mark.parametrize(
    "key, value",
    [
        ('name', 'КОТИК КОМАРУ'),
        ('photos', ["pic.jpg", "citty.jpg", "cat.jpg", "dog.jpg"]),
        ('location', 'SRID=4326;POINT(125.6 10.1)'),
        ('address', {"type": "Feature", "geometry": {"type": "Point", "coordinates": [90.6, 10.1]}, "properties": {"name": "Moscow"}})
    ]
)
async def test_change_property(key: Any, value: Any, create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    response_change = await test_app.patch(
        f"/v1_test/Restaurant/change_restaurant_property/{1}/{key}",
        json={'value': value}
    )
    assert response_change.status_code == 200
    async with get_session_test() as session:
        # получить измененное проперти
        if key != "location":
            stmt = (
                f"SELECT {key} FROM restaurants WHERE id = {1};"
            )
        else:
            stmt = (
                f"SELECT ST_AsEWKT(location) AS location FROM restaurants WHERE id = {1};"
            )
        result = await session.execute(text(stmt))
        actual_value = result.first()[0]
        assert actual_value == value