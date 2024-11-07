from fastapi import APIRouter, Depends

from src.models.dto.owner import OwnerRequest, OwnerResult, OwnerRequestUpdate
from src.service import get_owner_service, OwnerService

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

@owner_router.post("/create_owner/")
async def create_owner(
        model: OwnerRequest,
        service: OwnerService = Depends(get_owner_service)
) -> OwnerResult:
    return await service.create_owner(model)

@owner_router.put("/update_owner_name/")
async def update_owner_name(
        model: OwnerRequestUpdate,
        service: OwnerService = Depends(get_owner_service)
) -> OwnerResult:
    return await service.update_owner_name(model)