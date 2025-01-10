from fastapi import APIRouter, Depends

from src.models.dto.favourites import FavouriteCategoryDTO
from src.service.category import get_fav_category_service, FavouriteCategoriesService

fav_category_router = APIRouter(
    prefix="/FavouriteCategory",
    tags=["FavouriteCategory"]
)

@fav_category_router.get("/get_all_user_fav_categories/{user_id}")
async def get_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> list[str]:
    return await service.get_all_user_fav_categories(user_id)

@fav_category_router.delete("/drop_all_user_fav_categories/{user_id}")
async def drop_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    await service.drop_all_user_fav_categories(user_id)

@fav_category_router.post("/add_fav_category/")
async def add_fav_category(
        model: FavouriteCategoryDTO,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    await service.create(model)

@fav_category_router.delete("/delete_fav_category/{user_id}/{cat_name}")
async def delete_fav_category(
        user_id: int,
        cat_name: str,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    await service.delete(FavouriteCategoryDTO(user_id=user_id, cat_name=cat_name))

