from fastapi import APIRouter, Depends

from src.models.dto.favourites import AllFavouriteCategoriesRequest, FavouriteCategoryResponse, FavouriteCategoryDTO
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.service.category import FavouriteCategoriesService
from tests.sql_connector import get_session_test

fav_category_router = APIRouter(
    prefix="/FavouriteCategory",
    tags=["FavouriteCategory"]
)

def get_test_fav_category_service() -> FavouriteCategoriesService:
    return FavouriteCategoriesService(repo=FavouriteCategoryRepo(session_getter=get_session_test))


@fav_category_router.get("/get_all_user_fav_categories/{user_id}")
async def get_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_test_fav_category_service)
) -> list[FavouriteCategoryResponse]:
    return await service.get_all_user_fav_categories(model=AllFavouriteCategoriesRequest(user_id=user_id))

@fav_category_router.delete("/drop_all_user_fav_categories/{user_id}")
async def drop_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_test_fav_category_service)
) -> AllFavouriteCategoriesRequest:
    return await service.drop_all_user_fav_categories(model=AllFavouriteCategoriesRequest(user_id=user_id))

@fav_category_router.post("/add_fav_category/")
async def add_fav_category(
        model: FavouriteCategoryDTO,
        service: FavouriteCategoriesService = Depends(get_test_fav_category_service)
) -> FavouriteCategoryResponse:
    return await service.create(model)

@fav_category_router.delete("/delete_fav_category/{user_id}/{cat_name}")
async def delete_fav_category(
        user_id: int,
        cat_name: str,
        service: FavouriteCategoriesService = Depends(get_test_fav_category_service)
) -> FavouriteCategoryResponse:
    return await service.delete(FavouriteCategoryDTO(user_id=user_id, cat_name=cat_name))

