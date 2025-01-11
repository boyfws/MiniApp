from fastapi import APIRouter, Depends

from src.service.category import get_category_service, CategoryService

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)

@category_router.get(
    "/get_category_id/{category_name}",
    summary="Получить айди категории по названию"
)
async def get_category_id(
        category_name: str,
        service: CategoryService = Depends(get_category_service)
) -> int:
    """
    Получить айди категории по названию.
    """
    return await service.get(cat_name=category_name)

@category_router.get(
    "/get_all_categories/{user_id}",
    summary="Получить список всех категорий в базе"
)
async def get_all_categories(
        user_id: int,
        service: CategoryService = Depends(get_category_service)
) -> list[str]:
    """
    Получить список всех категорий в базе
    """
    return await service.get_all()
