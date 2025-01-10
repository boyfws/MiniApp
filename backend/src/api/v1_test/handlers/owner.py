from fastapi import APIRouter, Depends

from src.service import OwnerService
from tests.sql_connector import get_session_test

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

def get_test_owner_service() -> OwnerService:
    return OwnerService(session_getter=get_session_test)

@owner_router.get("/is_owner/{owner_id}")
async def is_owner(
        owner_id: int,
        service: OwnerService = Depends(get_test_owner_service)
) -> bool:
    return await service.is_owner(owner_id)