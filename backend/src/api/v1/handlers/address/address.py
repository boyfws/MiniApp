from fastapi import APIRouter, Depends, status

from src.models.dto.address import GeoJson
from src.service.address import get_address_service, transform_to_dto
from src.service.address import AddressService

address_router = APIRouter(
    prefix="/Address",
    tags=["Address"]
)

@address_router.post(
    "/add_address/",
    summary="Добавить новый адрес",
    status_code=status.HTTP_201_CREATED,
)
async def add_address(
        model: GeoJson,
        service: AddressService = Depends(get_address_service)
) -> int:
    """
    Добавить новый адрес в базу данных. Принимает объект по схеме GeoJson.
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
    Возвращает айди добавленного адреса в базе
    """
    return await service.add_address(transform_to_dto(model))
