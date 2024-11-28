from collections.abc import AsyncGenerator
from contextlib import _AsyncGeneratorContextManager
from typing import Callable, Optional

from src.database.mongo_db import AsyncMongoDB, get_db
from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID


class MenuRepository:
    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncMongoDB]] = get_db):
        """Вставьте сюда функцию, которая выдает сессию работы с базой данных"""
        self.session_getter=session_getter

    async def get_menu_by_rest_id(self, model: RestaurantRequestUsingID) -> Optional[MenuDTO]:
        async with self.session_getter() as session:
            menu_data = await session.menu.find_one({'restaurant_id': model.rest_id})
            if not menu_data:
                return None
            menu_data_without_id = {key: value for key, value in menu_data.items() if key != "_id"}
            return MenuDTO(**menu_data_without_id)

    async def update_menu_by_rest_id(self, model: MenuDTO) -> int:
        async with self.session_getter() as session:
            menu = model.model_dump(by_alias=True)
            await session.menu.update_one(
                {'restaurant_id': menu['restaurant_id']},
                {
                    '$set': {
                        'categories': menu['categories'],
                        "restaurant_description": menu['restaurant_description']
                    }
                },
                upsert=True  # Если ресторан не найден, создаем новый
            )
            return model.restaurant_id

    async def delete_menu_by_rest_id(self, model: RestaurantRequestUsingID) -> bool:
        async with self.session_getter() as session:
            result = await session.menu.delete_one({'restaurant_id': model.rest_id})
            return result.deleted_count > 0
