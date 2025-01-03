from fastapi import APIRouter, Depends

from src.models.dto.address_for_user import AddressForUserDTO, AddressesResponse, AllAddressesForUser
from src.service.address import AddressesForUserService
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
) -> list[AddressForUserDTO]:
    return await service.get_all_user_fav_restaurants(model=AllAddressesForUser(user_id=user_id))

@addresses_for_user_router.delete("/drop_all_addresses/{user_id}")
async def drop_all_addresses(
        user_id: int,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> AddressesResponse:
    return await service.drop_all_user_fav_restaurants(model=AllAddressesForUser(user_id=user_id))

@addresses_for_user_router.post("/add_address/")
async def add_address(
        model: AddressForUserDTO,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> AddressesResponse:
    return await service.create(model)

@addresses_for_user_router.delete("/delete_address/{user_id}/{address_id}")
async def delete_address(
        user_id: int,
        address_id: int,
        service: AddressesForUserService = Depends(get_test_address_for_user_service)
) -> AddressesResponse:
    return await service.delete(AddressForUserDTO(user_id=user_id, address_id=address_id))