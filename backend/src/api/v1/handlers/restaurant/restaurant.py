from fastapi import APIRouter, Depends, status

from src.models.dto.restaurant import (
    RestaurantRequestFullModel, RestaurantRequestUsingID,
    RestaurantRequestUsingGeoPointAndName, Point,
    RestaurantGeoSearch, RestaurantDTO, AnyField
)
from src.service.restaurant import get_restaurant_service, RestaurantService

restaurant_router = APIRouter(
    prefix="/Restaurant",
    tags=["Restaurant"]
)

@restaurant_router.post(
    "/create_restaurant/",
    summary="Создать ресторан"
)
async def create_restaurant(
        model: RestaurantRequestFullModel,
        service: RestaurantService = Depends(get_restaurant_service)
) -> int:
    """
    Создать ресторан. Принимает его модель по схеме RestaurantRequestFullModel.
    Пример json этой схемы:
    ```
    {
        owner_id: 1,
        name: 'kfc',
        main_photo: 'photo.jpg',
        photos: ['photo.jpg', 'pic.jpg', 'citty.jpg'],
        orig_phone: '77777777777',
        wapp_phone: '77777777777',
        location: "SRID=4326;POINT(125.6 10.1)",
        address: {"type": "Feature",
                 "geometry":
                     {"type": "Point",
                      "coordinates": [125.6, 10.1]},
                 "properties":
                     {"name": "Dinagat Islands"}},
        categories: [2, 3]
    }
    ```

    Возвращает айди добавленного ресторана.
    """
    return await service.create(model)

@restaurant_router.delete(
    "/delete_restaurant/{rest_id}/{user_id}",
    summary="Удалить ресторан",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_restaurant(
        rest_id: int,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> None:
    """
    Удалить ресторан. Принимает в путь url айди пользователя и ресторана.
    Ничего не возвращает.
    """
    return await service.delete(RestaurantRequestUsingID(rest_id=rest_id, user_id=user_id))

@restaurant_router.patch(
    "/update_restaurant/{rest_id}",
    summary="Обновить ресторан",
    status_code=status.HTTP_205_RESET_CONTENT
)
async def update_restaurant(
        rest_id: int,
        model: RestaurantRequestFullModel,
        service: RestaurantService = Depends(get_restaurant_service)
) -> None:
    """
    Обновить ресторан. Принимает ту же схему, что и запрос на добавление.
    Вы должны фактически прислать просто новую схему, которая заменит текущую по переданному rest_id.
    Ничего не возвращает.
    """
    await service.update(rest_id, model)

@restaurant_router.get(
    "/get_by_id/{rest_id}/{user_id}",
    summary="Получить ресторан",
)
async def get_restaurant_by_id(
        rest_id: int,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantDTO:
    """
    Получить ресторан. Принимает в путь url айди пользователя и ресторана.
    Вернет полную схему ресторана с дополнительной бизнес-логикой для пользователя.
    В данный момент там добавлено поле, которое характеризует, является ли ресторан любимым у пользователя.
    """
    return await service.get(RestaurantRequestUsingID(rest_id=rest_id, user_id=user_id))

@restaurant_router.get(
    "/get_by_owner/{owner_id}",
    summary="Получить рестораны владельца"
)
async def get_restaurant_by_owner(
        owner_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantRequestFullModel]:
    """
    Получить список ресторанов владельца. Принимает в путь url айди владельца.
    Возвращает список его ресторанов по схеме RestaurantRequestFullModel
    """
    return await service.get_by_owner(owner_id)

@restaurant_router.get(
    "/get_by_geo/{lon}/{lat}/{user_id}",
    summary="Поиск ресторанов по геолокации"
)
async def get_restaurant_by_geo(
        lon: float,
        lat: float,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantGeoSearch]:
    """
    Поиск ресторанов по геолокации. Принимает в путь url долготу, широту и айди пользователя.
    Айди пользователя позволяет бизнес-логики для пользователя.
    Вернет ресторан по схеме RestaurantGeoSearch.
    Пример возвращаемых данных:
    ```
    [
        {id: 1, name:'kfc', main_photo: 'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
        {id: 2, name: 'kfc', main_photo:'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
        {id: 3, name: 'kfc', main_photo: 'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
    ]
    ```
    """
    return await service.get_by_geo(model=Point(lon=lon, lat=lat), user_id=user_id)

@restaurant_router.get(
    "/get_by_geo_and_name/{lon}/{lat}/{name_pattern}/{user_id}",
    summary="Поиск ресторанов по геолокации и названию"
)
async def get_restaurant_by_geo_and_name(
        lon: float,
        lat: float,
        name_pattern: str,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantGeoSearch]:
    """
    Поиск ресторанов по геолокации и названию. Принимает в путь url долготу, широту, название и айди пользователя.
    Айди пользователя позволяет бизнес-логики для пользователя.
    Вернет ресторан по схеме RestaurantGeoSearch.
    Пример возвращаемых данных:
    ```
    [
        {id: 1, name:'kfc', main_photo: 'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
        {id: 2, name: 'kfc', main_photo:'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
        {id: 3, name: 'kfc', main_photo: 'photo.jpg', distance: 0, category: ["Суши", "Пицца"], favourite_flag: False, rating: null},
    ]
    ```
    """
    return await service.get_by_geo_and_name(
        model=RestaurantRequestUsingGeoPointAndName(
            point=Point(lon=lon, lat=lat),
            name_pattern=name_pattern
        ),
        user_id=user_id
    )

@restaurant_router.get(
    "/get_restaurant_name_by_id/{rest_id}",
    summary="Получить название ресторана по айди"
)
async def get_restaurant_name_by_id(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> str:
    """
    Получить название ресторана по айди.
    """
    return await service.get_name(rest_id)

@restaurant_router.get(
    "/get_restaurant_available_properties/{rest_id}",
    summary="Какие свойства ресторана заполнены"
)
async def get_restaurant_available_properties(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> dict[str, bool]:
    """
    Получить, какие свойства ресторана заполнены. Принимает айди ресторана.
    Возвращает словарь, где у каждого названия поля в таблице будет указан флаг того, что поле пусто.
    Пример возвращаемых данных:
    ```
    {
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
    ```
    """
    return await service.get_available_properties(rest_id)

@restaurant_router.patch(
    "/change_restaurant_property/{rest_id}/{key}",
    summary="Поменять свойство ресторана"
)
async def change_restaurant_property(
        rest_id: int,
        key: str,
        value: AnyField,
        service: RestaurantService = Depends(get_restaurant_service)
) -> None:
    """
    Поменять свойство ресторана. Принимает в путь url айди ресторана и название поля, которое требуется поменять.
    Также принимает в себя json с новым значением этого поля для корректной его передачи по сети.
    Пример входных данных:
    ```
    {
        'value': [
            "pic.jpg", "citty.jpg", "cat.jpg", "dog.jpg"
        ]
    }
    ```
    Ничего не возвращает.
    """
    await service.change_restaurant_property(rest_id, key, value.value)