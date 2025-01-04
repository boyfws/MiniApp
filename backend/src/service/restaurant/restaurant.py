from contextlib import _AsyncGeneratorContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql_session import get_session
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPointAndName, \
    RestaurantGeoSearch, Point, RestaurantDTO
from src.repository.restaurant.restaurant import RestaurantRepo


class RestaurantService:
    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]] = get_session) -> None:
        self.repo = RestaurantRepo(session_getter=session_getter)

    async def create(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        return await self.repo.create(model)

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        return await self.repo.delete(model)

    async def update(
            self,
            rest_id: int,
            model: RestaurantRequestFullModel
    ) -> None:
        await self.repo.update(rest_id=rest_id, model=model)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantDTO:
        return await self.repo.get(model)

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantDTO]:
        return await self.repo.get_by_owner(model)

    async def get_by_geo(
            self,
            user_id: int,
            model: Point
    ) -> list[RestaurantGeoSearch]:
        return await self.repo.get_by_geo(model=model, user_id=user_id)

    async def get_by_geo_and_name(
            self,
            user_id: int,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        return await self.repo.get_by_geo_and_name(model=model, user_id=user_id)

    async def get_name(self, rest_id: int) -> str:
        return await self.repo.get_name(rest_id)

    async def get_available_properties(self, rest_id: int) -> dict[str, bool]:
        rest_properties: RestaurantRequestFullModel = await self.get(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))
        list_properties = list(RestaurantRequestFullModel.__dict__['__annotations__'].keys())
        field_status = {}
        for field in list_properties:
            value = getattr(rest_properties, field)
            field_status[field] = value is not None

        return field_status

    async def change_restaurant_property(self, rest_id: int, key: str, value: str) -> None:
        await self.repo.change_restaurant_property(rest_id, key, value)

