from fastapi import APIRouter, Depends

from src.models.dto.address import AddressResult, AddressDTO, AddressRequest
from src.service.tables.address import get_address_service
from src.service.tables.address.address import AddressService

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

@address_router.delete("/delete_address")
async def delete_address(
        model: AddressRequest,
        service: AddressService = Depends(get_address_service)
) -> AddressResult:
    return await service.delete(model)