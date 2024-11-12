from pydantic import BaseModel

from src.database.mongo_db import AsyncMongoDB
from src.models.dto.restaurant import RestaurantRequestUsingID

class MenuDTO(BaseModel):
    ...

class MenuRepository:
    async def get_menu_by_rest_id(self, session: AsyncMongoDB, model: RestaurantRequestUsingID) -> MenuDTO:
        ...

    async def update_menu_by_rest_id(self, session: AsyncMongoDB, model: MenuDTO) -> int:
        ...

    async def delete_menu_by_rest_id(self, session: AsyncMongoDB, model: RestaurantRequestUsingID) -> None:
        ...

    async def create_menu(self, session: AsyncMongoDB, model: MenuDTO) -> None:
        ...
