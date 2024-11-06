from fastapi import APIRouter, Depends

from src.models.dto.category import CategoryRequestUpdate, CategoryResult
from src.service.tables.category import get_category_service, CategoryService

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
        name: str,
        service: CategoryService = Depends(get_category_service)
):
    ...


@category_router.post("/add_category/")
async def add_category(
        name: str,
        service: CategoryService = Depends(get_category_service)
):
    ...

@category_router.get("/get_category_id")
async def get_category_id(
        name: str,
        service: CategoryService = Depends(get_category_service)
):
    ...
