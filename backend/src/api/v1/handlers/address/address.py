from fastapi import APIRouter, Depends

from src.models.dto.address import AddressResult, AddressDTO, AddressRequest
from src.service.address import get_address_service
from src.service.address import AddressService

address_router = APIRouter(
    prefix="/Address",
    tags=["Address"]
)

@address_router.post("/add_address/")
async def add_address(
        model: AddressDTO,
        service: AddressService = Depends(get_address_service)
) -> AddressResult:
    return await service.add_address(model)

@address_router.delete("/delete_address/{address_id}")
async def delete_address(
        address_id: int,
        service: AddressService = Depends(get_address_service)
) -> AddressResult:
    return await service.delete(AddressRequest(id=address_id))