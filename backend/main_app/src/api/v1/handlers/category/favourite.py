from fastapi import APIRouter, Depends

from src.models.dto.favourites import AllFavouriteCategoriesRequest, FavouriteCategoryResponse, FavouriteCategoryDTO
from src.service.category import get_fav_category_service, FavouriteCategoriesService

fav_category_router = APIRouter(
    prefix="/FavouriteCategory",
    tags=["FavouriteCategory"]
)

@fav_category_router.get("/get_all_user_fav_categories/")
async def get_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> list[FavouriteCategoryResponse]:
    return await service.get_all_user_fav_categories(model=model)

@fav_category_router.delete("/drop_all_user_fav_categories/")
async def drop_all_user_fav_categories(
        model: AllFavouriteCategoriesRequest,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> AllFavouriteCategoriesRequest:
    return await service.drop_all_user_fav_categories(model=model)

@fav_category_router.post("/add_fav_category/")
async def add_fav_category(
        model: FavouriteCategoryDTO,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> FavouriteCategoryResponse:
    return await service.create(model)

@fav_category_router.delete("/delete_fav_category/")
async def delete_fav_category(
        model: FavouriteCategoryDTO,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> FavouriteCategoryResponse:
    return await service.delete(model)

