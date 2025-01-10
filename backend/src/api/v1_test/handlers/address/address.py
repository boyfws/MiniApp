from fastapi import APIRouter, Depends

from src.models.dto.address import AddressDTO, AddressRequest
from src.repository.address.address import AddressRepo
from src.service.address import AddressService
from tests.sql_connector import get_session_test

address_router = APIRouter(
    prefix="/Address",
    tags=["Address"]
)

def get_test_address_service() -> AddressService:
    return AddressService(repo=AddressRepo(session_getter=get_session_test))


@address_router.post("/add_address/")
async def add_address(
        model: AddressDTO,
        service: AddressService = Depends(get_test_address_service)
) -> int:
    return await service.add_address(model)

@address_router.delete("/delete_address/{address_id}")
async def delete_address(
        address_id: int,
        service: AddressService = Depends(get_test_address_service)
) -> None:
    await service.delete(AddressRequest(id=address_id))