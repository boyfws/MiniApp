from fastapi import APIRouter, Depends

from src.models.dto.category import CategoryRequestByName, CategoryResult, CategoryDTO
from src.service.category import get_category_service, CategoryService

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)


@category_router.post("/add_category/")
async def add_category(
        model: CategoryDTO,
        service: CategoryService = Depends(get_category_service)
) -> CategoryResult:
    return await service.create(model)

@category_router.get("/get_category_id/")
async def get_category_id(
        model: CategoryRequestByName,
        service: CategoryService = Depends(get_category_service)
) -> CategoryDTO:
    return await service.get(model)

