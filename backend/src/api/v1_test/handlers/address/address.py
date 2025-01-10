from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.models.dto.address import AddressDTO
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

@address_router.delete("/delete_address")
async def delete_address(
        region: Optional[str] = Query(default=None),
        city: str = Query(...),
        district: Optional[str] = Query(default=None),
        street: Optional[str] = Query(default=None),
        house: Optional[str] = Query(default=None),
        location: str = Query(...),
        service: AddressService = Depends(get_test_address_service)
) -> None:
    await service.delete(
        AddressDTO(
            region=region, city=city, district=district,
            street=street, house=house, location=location
        )
    )