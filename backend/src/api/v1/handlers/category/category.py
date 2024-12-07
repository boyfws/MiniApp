from fastapi import APIRouter, Depends

from src.models.dto.category import CategoryResult, CategoryDTO
from src.service.category import get_category_service, CategoryService

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)

@category_router.get("/get_category_id/{category_name}")
async def get_category_id(
        category_name: str,
        service: CategoryService = Depends(get_category_service)
) -> CategoryResult:
    return await service.get(CategoryDTO(name=category_name))

@category_router.get("/get_all_categories/")
async def get_all_categories(
        service: CategoryService = Depends(get_category_service)
) -> list[CategoryDTO]:
    return await service.get_all()
