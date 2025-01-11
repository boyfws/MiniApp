from fastapi import APIRouter, Depends, Query, status
from typing import Any, Optional

from src.models.dto.address import GeoJson
from src.models.dto.address_for_user import DeleteAddressForUser
from src.service.address import AddressesForUserService, get_address_for_user_service, transform_to_dto

addresses_for_user_router = APIRouter(
    prefix="/AddressesForUser",
    tags=["AddressesForUser"]
)

@addresses_for_user_router.get(
    "/get_all_addresses/{user_id}",
    summary="Получить все адреса пользователя"
)
async def get_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> list[GeoJson]:
    """
    Получить все адреса пользователя. Принимает айди.
    Возвращает данные по схеме GeoJson.
    """
    return await service.get_all_user_addresses(user_id=user_id)


@addresses_for_user_router.delete(
    "/drop_all_addresses/{user_id}",
    summary="Удалить все адреса пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def drop_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> None:
    """
    Удалить все адреса пользователя. Принимает айди.
    Ничего не возвращает.
    """
    await service.drop_all_user_fav_restaurants(user_id=user_id)

@addresses_for_user_router.post(
    "/add_address/{user_id}",
    summary="Добавить адрес пользователю",
    status_code=status.HTTP_201_CREATED
)
async def add_address(
        user_id: int,
        model: GeoJson,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> None:
    """
    Добавить адрес пользователю. Принимает в url путь айди, а также модель по схеме GeoJson.
    Пример входного json:
    ```
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                37.552687,
                55.777013
            ]
        },
        "properties": {
            "city": "Москва",
            "region": null,
            "street": "улица Поликарпова",
            "district": null,
            "house": "8"
        }
    }
    ```
    Ничего не возвращает.
    """
    await service.create(user_id, transform_to_dto(model))

@addresses_for_user_router.delete(
    "/delete_address/{user_id}",
    summary="Удалить адрес пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_address(
        user_id: int,
        region: Optional[str] = Query(default=None),
        city: str = Query(...),
        district: Optional[str] = Query(default=None),
        street: Optional[str] = Query(default=None),
        house: Optional[str] = Query(default=None),
        location: str = Query(...),
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> None:
    """
    Удалить адрес пользователя. Принимает в путь url айди пользователя, а в параметры запроса свойства адреса.
    Пример запроса:
    ```
    /v1/AddressesForUser/delete_address/{user_id}?
    &region={"Республика Чечня"}
    &city={"Санкт-Петербург"}
    &district={"Красноярск"}
    &street={"улица Аникутина"}
    &house={"12"}
    &location={"SRID=4326;POINT(37.617 55.755)"}
    ```
    Ничего не возвращает.
    """
    await service.delete(
        DeleteAddressForUser(
            user_id=user_id, region=region, city=city, district=district,
            street=street, house=house, location=location
        )
    )