from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.models.dto.address import GeoJson
from src.models.dto.address_for_user import DeleteAddressForUser
from src.service.address import AddressesForUserService, transform_to_dto
from tests.sql_connector import get_session_test

addresses_for_user_router = APIRouter(
    prefix="/AddressesForUser",
    tags=["AddressesForUser"]
)

def get_test_address_for_user_service() -> AddressesForUserService:
    return AddressesForUserService(session_getter=get_session_test)

@addresses_for_user_router.get("/get_all_addresses/{user_id}")
async def get_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> list[GeoJson]:
    return await service.get_all_user_addresses(user_id=user_id)

@addresses_for_user_router.delete("/drop_all_addresses/{user_id}")
async def drop_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> None:
    await service.drop_all_user_fav_restaurants(user_id=user_id)

@addresses_for_user_router.post("/add_address/{user_id}")
async def add_address(
        user_id: int,
        model: GeoJson,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> None:
    await service.create(user_id, transform_to_dto(model))

@addresses_for_user_router.delete("/delete_address/{user_id}")
async def delete_address(
        user_id: int,
        region: Optional[str] = Query(default=None),
        city: str = Query(...),
        district: Optional[str] = Query(default=None),
        street: Optional[str] = Query(default=None),
        house: Optional[str] = Query(default=None),
        location: str = Query(...),
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> None:
    await service.delete(
        DeleteAddressForUser(
            user_id=user_id, region=region, city=city, district=district,
            street=street, house=house, location=location
        )
    )