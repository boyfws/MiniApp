from fastapi import APIRouter, Depends
from typing import Any, Optional

from src.models.dto.address import GeoJson
from src.models.dto.address_for_user import AddressForUserDTO, AddressesResponse, AllAddressesForUser
from src.service.address import AddressesForUserService, get_address_for_user_service, transform_to_dto

addresses_for_user_router = APIRouter(
    prefix="/AddressesForUser",
    tags=["AddressesForUser"]
)

@addresses_for_user_router.get("/get_all_addresses/{user_id}")
async def get_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> list[Optional[GeoJson]]:
    address_dto = await service.get_all_user_addresses(model=AllAddressesForUser(user_id=user_id))
    result = []
    for address in address_dto:
        point_str = address.location.split(';')[1].split('(')[1].split(')')[0]
        coordinates = [float(x) for x in point_str.split()]
        result.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coordinates},
            "properties": {key: value for key, value in address.model_dump().items() if key != "location"}
        })
    return result

@addresses_for_user_router.delete("/drop_all_addresses/{user_id}")
async def drop_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> AddressesResponse:
    return await service.drop_all_user_fav_restaurants(model=AllAddressesForUser(user_id=user_id))

@addresses_for_user_router.post("/add_address/{user_id}")
async def add_address(
        user_id: int,
        model: GeoJson,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> AddressesResponse:
    return await service.create(user_id, transform_to_dto(model))

@addresses_for_user_router.delete("/delete_address/{user_id}/{address_id}")
async def delete_address(
        user_id: int,
        address_id: int,
        service: AddressesForUserService = Depends(get_address_for_user_service)
) -> AddressesResponse:
    return await service.delete(AddressForUserDTO(user_id=user_id, address_id=address_id))