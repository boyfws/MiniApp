from fastapi import APIRouter, Depends

from src.service import OwnerService, get_owner_service
from tests.sql_connector import get_session_test

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

def get_test_owner_service() -> OwnerService:
    return OwnerService(session_getter=get_session_test)

@owner_router.post("/create_owner/{owner_id}")
async def create_owner(
        owner_id: int,
        service: OwnerService = Depends(get_test_owner_service)
) -> None:
    await service.create_owner(owner_id)