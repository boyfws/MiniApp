from fastapi import APIRouter, Depends, status

from src.models.dto.favourites import FavouriteRestaurantDTO
from src.service.restaurant import get_fav_restaurant_service, FavouriteRestaurantService

fav_restaurant_router = APIRouter(
    prefix="/FavouriteRestaurant",
    tags=["FavouriteRestaurant"]
)

@fav_restaurant_router.get(
    "/get_all_user_fav_restaurants/{user_id}",
    summary="Получить все любимые рестораны пользователя"
)
async def get_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> list[int]:
    """
    Получить все любимые рестораны пользователя. Принимает в url путь айди пользователя.
    Возвращает список айди его любимых ресторанов.
    """
    return await service.get_all_user_fav_restaurants(user_id)

@fav_restaurant_router.delete(
    "/drop_all_user_fav_restaurants/{user_id}",
    summary="Удалить все любимые рестораны пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def drop_all_user_fav_restaurants(
        user_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> None:
    """
    Удалить все любимые рестораны пользователя. Принимает в url путь айди пользователя.
    Ничего не возвращает.
    """
    return await service.drop_all_user_fav_restaurants(user_id)

@fav_restaurant_router.post(
    "/add_fav_restaurant/",
    summary="Добавить любимый ресторан пользователю",
    status_code=status.HTTP_201_CREATED
)
async def add_fav_restaurant(
        model: FavouriteRestaurantDTO,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> None:
    """
    Добавить любимый ресторан пользователю. Принимает модель по схеме FavouriteRestaurantDTO.
    Ничего не возвращает.
    """
    await service.create(model)

@fav_restaurant_router.delete(
    "/delete_fav_restaurant/{user_id}/{rest_id}",
    summary="Удалить любимый ресторан пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_fav_restaurant(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> None:
    """
    Удалить любимый ресторан пользователя. Принимает в путь url айди пользователя и ресторана.
    Ничего не возвращает.
    """
    return await service.delete(FavouriteRestaurantDTO(user_id=user_id, rest_id=rest_id))

@fav_restaurant_router.get(
    "/check_is_favourite/{user_id}/{rest_id}",
    summary="Проверить, что ресторан входит в любимые",
)
async def check_is_favourite(
        user_id: int,
        rest_id: int,
        service: FavouriteRestaurantService = Depends(get_fav_restaurant_service)
) -> bool:
    """
    Проверить, что ресторан входит в любимые. Принимает в путь url айди пользователя и ресторана.
    Возвращает ответ в формате булевого значения.
    """
    return await service.is_favourite(user_id, rest_id)