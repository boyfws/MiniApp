import pytest
from sqlalchemy import text

from src.models.dto.address import GeoJson
from tests.common.address import geojson, get_addresses, get_dicts
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.test_repository.test_address.test_addresses_for_user import create_db_values_1, truncate_db, create_db_values_2
from tests.test_service.test_address.test_addresses_for_user import address_for_user_service


@pytest.mark.parametrize(
    "user_id, model",
    [
        (1, geojson()[0]),
        (1, geojson()[1])
    ]
)
async def test_add_address_for_user(user_id: int, model: GeoJson, test_app, create_db_values_1, truncate_db):
    response = await test_app.post(f'/v1_test/AddressesForUser/add_address/{user_id}', json=model.model_dump())
    assert response.status_code == 200

@pytest.mark.parametrize(
    "user_id",
    [
        1
    ]
)
async def test_delete(user_id: int, test_app, create_db_values_2, truncate_db):
    response = await test_app.delete(
        f'/v1_test/AddressesForUser/delete_address/{user_id}'
        f'?&region={"Республика Чечня"}&city={"Санкт-Петербург"}&district={"Красноярск"}&street={"улица Аникутина"}&house={"12"}&location={"SRID=4326;POINT(37.617 55.755)"}'

    )
    assert response.status_code == 200
    assert [get_addresses()[2]] == await address_for_user_service.get_all_user_addresses(1)

@pytest.mark.parametrize(
    "user_id, expected_list_result",
    [
        (1, get_dicts()),
        (1000, [])
    ]
)
async def test_get_all_user_addresses(
        user_id: int,
        expected_list_result: list[GeoJson],
        test_app, create_db_values_2, truncate_db): # fixtures
    response = await test_app.get(f'/v1_test/AddressesForUser/get_all_addresses/{user_id}')
    assert response.status_code == 200
    assert response.json() == expected_list_result

@pytest.mark.parametrize("user_id", [1, 1000])
async def test_drop_all_user_addresses(
        user_id: int,
        test_app, create_db_values_2, truncate_db):
    response = await test_app.delete(f'/v1_test/AddressesForUser/drop_all_addresses/{user_id}')
    assert response.status_code == 200
    async with get_session_test() as session:
        count = await session.execute(text(f"SELECT COUNT(*) FROM addresses_for_user WHERE user_id = {user_id}"))
        assert count.scalar() == 0