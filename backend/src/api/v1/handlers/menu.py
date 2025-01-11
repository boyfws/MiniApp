from typing import Optional

from fastapi import APIRouter, Depends, status

from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID
from src.service import get_menu_service
from src.service.menu import MenuService

menu_router = APIRouter(
    prefix="/Menu",
    tags=["Menu"]
)

@menu_router.get(
    '/get_menu_by_rest_id/{rest_id}',
    summary="Получить меню ресторана"
)
async def get_menu_by_rest_id(
        rest_id: int,
        service: MenuService = Depends(get_menu_service)
) -> Optional[MenuDTO]:
    """
    Получить меню ресторана. Принимает айди ресторана в путь url.
    """
    return await service.get_menu_by_rest_id(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))

@menu_router.post(
    '/update_menu_by_rest_id/',
    summary="Обновить меню ресторана",
    status_code=status.HTTP_201_CREATED
)
async def update_menu_by_rest_id(
        model: MenuDTO,
        service: MenuService = Depends(get_menu_service)
) -> None:
    """
    Обновить меню ресторана. Принимает модель меню ресторана по схеме MenuDTO.
    Пример входного json:
    ```
    {
        'restaurant_id': 1,
        'categories': [
            {
                'category_name': 'Напитки',
                'items': [
                    {
                        'Name': 'Белое вино',
                        'Price': [375.0, 1500.0],
                        'Description': None,
                        'Condition': 'цена за бокал и бутылку'
                    },
                    {
                        'Name': 'Коктейли',
                        'Price': [500.0],
                        'Description': 'Авторские коктейли от бармена',
                        'Condition': 'покупка от 3 коктейлей'
                    }
                ]
            }
        ],
        'restaurant_description': 'ресторан где можно выпить вино и коктейли'
    }
    ```
    Ничего не возвращает.
    """
    await service.update_menu_by_rest_id(model)

@menu_router.delete(
    '/delete_menu_by_rest_id/{rest_id}',
    summary="Удалить меню ресторана",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_menu_by_rest_id(
        rest_id: int,
        service: MenuService = Depends(get_menu_service)
) -> None:
    """
    Удалить меню ресторана. Принимает айди ресторана в путь url.
    Ничего не возвращает.
    """
    await service.delete_menu_by_rest_id(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))