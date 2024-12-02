from fastapi import APIRouter, Depends

from src.service import OwnerService, get_owner_service

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

@owner_router.post("/create_owner/")
async def create_owner(
        owner_id: int,
        service: OwnerService = Depends(get_owner_service)
) -> None:
    await service.create_owner(owner_id)