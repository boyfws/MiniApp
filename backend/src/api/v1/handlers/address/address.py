from fastapi import APIRouter, Depends

from src.api.v1.handlers.yandex_api.GeoCode import GeoJson
from src.models.dto.address import AddressResult, AddressDTO, AddressRequest
from src.service.address import get_address_service
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
    address = model.get("properties")
    coordinates = model.get("geometry").get("coordinates")
    location = f"SRID=4326;POINT({coordinates[0]} {coordinates[1]})"
    result = AddressDTO(
        location=location,
        region=address.get('region'),
        city=address.get('street'),
        district=address.get('district'),
        street=address.get('street'),
        house=address.get('house')
    )
    return await service.add_address(result)

@address_router.delete("/delete_address/{address_id}")
async def delete_address(
        address_id: int,
        service: AddressService = Depends(get_address_service)
) -> AddressResult:
    return await service.delete(AddressRequest(id=address_id))