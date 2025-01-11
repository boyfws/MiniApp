from fastapi import APIRouter, Depends

from src.service import OwnerService, get_owner_service

owner_router = APIRouter(
    prefix="/Owner",
    tags=["Owner"]
)

@owner_router.get(
    "/is_owner/{owner_id}",
    summary="Является ли владельцем"
)
async def is_owner(
        owner_id: int,
        service: OwnerService = Depends(get_owner_service)
) -> bool:
    """
    Принимает айди владельца.
    Возвращает булево значение о том, есть ли в базе данных владелец с данным айди.
    """
    return await service.is_owner(owner_id)