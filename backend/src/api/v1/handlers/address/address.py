from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.models.dto.address import AddressDTO, GeoJson
from src.service.address import get_address_service, transform_to_dto
from src.service.address import AddressService

address_router = APIRouter(
    prefix="/Address",
    tags=["Address"]
)

@address_router.post("/add_address/")
async def add_address(
        model: GeoJson,
        service: AddressService = Depends(get_address_service)
) -> int:
    return await service.add_address(transform_to_dto(model))
