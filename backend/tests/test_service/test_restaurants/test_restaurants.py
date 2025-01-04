import pytest

from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantRequestUsingID, Point, \
    RestaurantRequestUsingGeoPointAndName, RestaurantRequestUsingOwner
from src.service.restaurant.restaurant import RestaurantService
from tests.common.restaurants import restaurants, get_search_result
from tests.sql_connector import get_session_test
from tests.test_repository.restaurants.test_restaurant import  truncate_db, create_categories_and_owner

restaurant_service = RestaurantService(session_getter=get_session_test)

@pytest.mark.parametrize(
    "model, expected_id",
    [(restaurants()[0], 1), (restaurants()[1], 1)]
)
async def test_create(
        model: RestaurantRequestFullModel,
        expected_id: int,
        create_categories_and_owner,
        truncate_db
):
    result = await restaurant_service.create(model)
    assert result.rest_id == expected_id

async def test_delete(create_categories_and_owner, truncate_db):
    inserted_id = await restaurant_service.create(restaurants()[0])
    result = await restaurant_service.delete(RestaurantRequestUsingID(rest_id=inserted_id.rest_id, user_id=1))
    assert result.rest_id == inserted_id.rest_id


async def test_update(create_categories_and_owner, truncate_db):
    inserted_id = await restaurant_service.create(restaurants()[0])
    await restaurant_service.update(inserted_id.rest_id, restaurants()[1])


async def test_get(create_categories_and_owner, truncate_db):
    inserted_id = await restaurant_service.create(restaurants()[0])
    rest = await restaurant_service.get(RestaurantRequestUsingID(rest_id=inserted_id.rest_id, user_id=1))
    expected = restaurants()[0].model_dump()
    expected['favourite_flag'] = False
    assert rest.model_dump() == expected

async def test_get_by_geo(create_categories_and_owner, truncate_db):
    await restaurant_service.create(restaurants()[0])
    await restaurant_service.create(restaurants()[0])
    await restaurant_service.create(restaurants()[0])
    # получить список ресторанов
    rest_list = await restaurant_service.get_by_geo(user_id=1, model=Point(lon=125.6, lat=10.1))
    assert rest_list == get_search_result()

async def test_get_by_geo_and_name(create_categories_and_owner, truncate_db):
    # создали 3 ресторана
    await restaurant_service.create(restaurants()[0])
    await restaurant_service.create(restaurants()[0])
    await restaurant_service.create(restaurants()[0])
    # получить список ресторанов
    rest_list = await restaurant_service.get_by_geo_and_name(
        user_id=1, model=RestaurantRequestUsingGeoPointAndName(point=Point(lon=125.6, lat=10.1), name_pattern='kf')
    )
    assert rest_list == get_search_result()

# async def test_get_by_owner(create_categories_and_owner, truncate_db):
#     await restaurant_service.create(restaurants()[0])
#     await restaurant_service.create(restaurants()[1])
#
#     # получить список всех рестиков у овнера 1
#     rest_list = await restaurant_service.get_by_owner(
#         RestaurantRequestUsingOwner(owner_id=1)
#     )
#     expected_1, expected_2 = restaurants()[0].model_dump(), restaurants()[1].model_dump()
#     expected_1['favourite_flag'] = True
#     expected_2['favourite_flag'] = True
#     assert [rest_list[0].model_dump(), rest_list[1].model_dump()] == [expected_1, expected_2]


async def test_get_name(create_categories_and_owner, truncate_db):
    rest_id = await restaurant_service.create(restaurants()[0])
    rest_name = await restaurant_service.get_name(rest_id.rest_id)
    assert rest_name == 'kfc'

async def test_get_properties(create_categories_and_owner, truncate_db):
    rest_id = await restaurant_service.create(restaurants()[0])
    result = await restaurant_service.get_available_properties(rest_id.rest_id)
    assert result == {
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