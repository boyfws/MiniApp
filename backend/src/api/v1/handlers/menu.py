from typing import Optional

from fastapi import APIRouter, Depends

from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID
from src.service import get_menu_service
from src.service.menu import MenuService

menu_router = APIRouter(
    prefix="/Menu",
    tags=["Menu"]
)

@menu_router.get('/get_menu_by_rest_id/{rest_id}')
async def get_menu_by_rest_id(
        rest_id: int,
        service: MenuService = Depends(get_menu_service)
) -> Optional[MenuDTO]:
    return await service.get_menu_by_rest_id(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))

@menu_router.post('/update_menu_by_rest_id/')
async def update_menu_by_rest_id(
        model: MenuDTO,
        service: MenuService = Depends(get_menu_service)
) -> int:
    return await service.update_menu_by_rest_id(model)

@menu_router.delete('/delete_menu_by_rest_id/{rest_id}')
async def delete_menu_by_rest_id(
        rest_id: int,
        service: MenuService = Depends(get_menu_service)
) -> bool:
    return await service.delete_menu_by_rest_id(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))