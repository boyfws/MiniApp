from fastapi import APIRouter, Depends

from src.repository.category.category import CategoryRepo
from src.service.category import CategoryService
from tests.sql_connector import get_session_test

category_router = APIRouter(
    prefix="/Category",
    tags=["Category"]
)

def get_test_category_service() -> CategoryService:
    return CategoryService(repo=CategoryRepo(session_getter=get_session_test))

@category_router.get("/get_category_id/{category_name}")
async def get_category_id(
        category_name: str,
        service: CategoryService = Depends(get_test_category_service)
) -> int:
    return await service.get(cat_name=category_name)

@category_router.get("/get_all_categories/{user_id}")
async def get_all_categories(
        user_id: int,
        service: CategoryService = Depends(get_test_category_service)
) -> list[str]:
    return await service.get_all()
