from contextlib import _AsyncGeneratorContextManager
from typing import Optional, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.mongo_db import get_db, AsyncMongoDB
from src.models.dto.menu import MenuDTO
from src.models.dto.restaurant import RestaurantRequestUsingID
from src.repository.menu import MenuRepository


class MenuService:
    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncMongoDB]] = get_db) -> None:
        self.repo = MenuRepository(session_getter)

    async def get_menu_by_rest_id(self, model: RestaurantRequestUsingID) -> Optional[MenuDTO]:
        return await self.repo.get_menu_by_rest_id(model)

    async def update_menu_by_rest_id(self, model: MenuDTO) -> int:
        return await self.repo.update_menu_by_rest_id(model)

    async def delete_menu_by_rest_id(self, model: RestaurantRequestUsingID) -> bool:
        return await self.repo.delete_menu_by_rest_id(model)