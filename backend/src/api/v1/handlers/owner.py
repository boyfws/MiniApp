from fastapi import APIRouter, Depends

from src.service import OwnerService, get_owner_service

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

@owner_router.get("/is_owner/{owner_id}")
async def is_owner(
        owner_id: int,
        service: OwnerService = Depends(get_owner_service)
) -> bool:
    return await service.is_owner(owner_id)