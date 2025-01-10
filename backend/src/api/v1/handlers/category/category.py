from fastapi import APIRouter, Depends

from src.service.category import get_category_service, CategoryService

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)

@category_router.get("/get_category_id/{category_name}")
async def get_category_id(
        category_name: str,
        service: CategoryService = Depends(get_category_service)
) -> int:
    return await service.get(cat_name=category_name)

@category_router.get("/get_all_categories/{user_id}")
async def get_all_categories(
        user_id: int,
        service: CategoryService = Depends(get_category_service)
) -> list[str]:
    return await service.get_all()
