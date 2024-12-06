import pytest
from sqlalchemy import text

from src.models.dto.restaurant import RestaurantRequestFullModel
from tests.common.restaurants import restaurants, get_search_result
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.test_repository.restaurants.test_restaurant import create_categories_and_owner, truncate_db


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
    assert response.json()['rest_id'] == expected_id

async def test_delete(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()['rest_id']
    result = await test_app.delete(f'/v1_test/Restaurant/delete_restaurant/{inserted_id}')
    assert result.status_code == 200
    delete_result_id = result.json()['rest_id']
    assert delete_result_id ==  inserted_id
    async with get_session_test() as session:
        count = await session.execute(text(f"SELECT COUNT(*) FROM restaurants WHERE id = {delete_result_id}"))
        assert count.scalar() == 0

async def test_update(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()['rest_id']
    result = await test_app.patch(f'/v1_test/Restaurant/update_restaurant/{inserted_id}', json=restaurants()[0].model_dump())
    assert result.status_code == 200

async def test_get(create_categories_and_owner, truncate_db, test_app):
    response = await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    assert response.status_code == 200
    inserted_id = response.json()['rest_id']
    result = await test_app.get(f"/v1_test/Restaurant/get_by_id/{inserted_id}")
    assert result.status_code == 200
    assert result.json() == restaurants()[0].model_dump()

async def test_get_by_geo(create_categories_and_owner, truncate_db, test_app):
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())

    rest_list_response = await test_app.get(f"/v1_test/Restaurant/get_by_geo/{30}/{60}")
    assert rest_list_response.status_code == 200
    assert rest_list_response.json() == [data.model_dump() for data in get_search_result()]

async def test_get_by_geo_and_name(create_categories_and_owner, truncate_db, test_app):
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())
    await test_app.post('/v1_test/Restaurant/create_restaurant/', json=restaurants()[0].model_dump())

    rest_list_response = await test_app.get(f"/v1_test/Restaurant/get_by_geo_and_name/{30}/{60}/{'kf'}")
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
    rest_id = response.json()['rest_id']
    result = await test_app.get(f"/v1_test/Restaurant/get_restaurant_name_by_id/{rest_id}")
    assert result.status_code == 200
    assert result.json() == 'kfc'