from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.models.dto.address import AddressResult, AddressDTO, AddressRequest, GeoJson
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
) -> AddressResult:
    return await service.add_address(transform_to_dto(model))

@address_router.delete("/delete_address")
async def delete_address(
        region: Optional[str] = Query(default=None),
        city: str = Query(...),
        district: Optional[str] = Query(default=None),
        street: Optional[str] = Query(default=None),
        house: Optional[str] = Query(default=None),
        location: str = Query(...),
        service: AddressService = Depends(get_address_service)
) -> AddressResult:
    return await service.delete(
        AddressDTO(
            region=region, city=city, district=district,
            street=street, house=house, location=location
        )
    )