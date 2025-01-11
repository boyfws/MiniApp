from fastapi import APIRouter, Depends, status

from src.models.dto.favourites import FavouriteCategoryDTO
from src.service.category import get_fav_category_service, FavouriteCategoriesService

fav_category_router = APIRouter(
    prefix="/FavouriteCategory",
    tags=["FavouriteCategory"]
)

@fav_category_router.get(
    "/get_all_user_fav_categories/{user_id}",
    summary="Получить все любимые категории пользователя"
)
async def get_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> list[str]:
    """
    Получить все любимые категории пользователя. Принимает в url путь только айди пользователя.
    Возвращает список строк - названий категорий, которые любимые у данного пользователя.
    """
    return await service.get_all_user_fav_categories(user_id)

@fav_category_router.delete(
    "/drop_all_user_fav_categories/{user_id}",
    summary="Удалить все любимые категории пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def drop_all_user_fav_categories(
        user_id: int,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    """
    Удалить все любимые категории пользователя. Принимает в url путь только айди пользователя.
    Ничего не возвращает.
    """
    await service.drop_all_user_fav_categories(user_id)

@fav_category_router.post(
    "/add_fav_category/",
    summary="Добавить любимую категорию пользователю",
    status_code=status.HTTP_201_CREATED
)
async def add_fav_category(
        model: FavouriteCategoryDTO,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    """
    Добавить любимую категорию пользователю. Принимает модель по схеме FavouriteCategoryDTO.
    Пример json такой модели:
    ```
    {
        user_id=1,
        cat_name="Бургеры"
    }
    ```
    Ничего не возвращает.
    """
    await service.create(model)

@fav_category_router.delete(
    "/delete_fav_category/{user_id}/{cat_name}",
    summary="Удалить любимую категорию пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_fav_category(
        user_id: int,
        cat_name: str,
        service: FavouriteCategoriesService = Depends(get_fav_category_service)
) -> None:
    """
    Удалить любимую категорию пользователя. Принимает в url путь название и айди пользователя.
    Пример json такой модели:
    ```
    {
        user_id=1,
        cat_name="Бургеры"
    }
    ```
    Ничего не возвращает.
    """
    await service.delete(FavouriteCategoryDTO(user_id=user_id, cat_name=cat_name))

