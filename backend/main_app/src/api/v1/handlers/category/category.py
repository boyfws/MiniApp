from fastapi import APIRouter, Depends

from src.models.dto.category import CategoryRequestUpdate, CategoryResult, CategoryDTO, CategoryRequest
from src.service.category import get_category_service, CategoryService

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)


@category_router.put("/update_category_name/")
async def update_category_name(
        model: CategoryRequestUpdate,
        service: CategoryService = Depends(get_category_service)
) -> CategoryResult:
    return await service.update(model=model)


@category_router.delete("/delete_category/")
async def delete_category(
        model: CategoryRequest,
        service: CategoryService = Depends(get_category_service)
) -> CategoryResult:
    return await service.delete(model)



@category_router.post("/add_category/")
async def add_category(
        model: CategoryRequest,
        service: CategoryService = Depends(get_category_service)
) -> CategoryResult:
    return await service.create(model)

@category_router.get("/get_category_id")
async def get_category_id(
        model: CategoryRequest,
        service: CategoryService = Depends(get_category_service)
) -> CategoryDTO:
    return await service.get(model)

