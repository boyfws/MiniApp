from contextlib import _AsyncGeneratorContextManager
from typing import Callable, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql_session import get_session
from src.models.dto.category import CategoryDTO
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPointAndName, \
    RestaurantGeoSearch, Point, RestaurantDTO, RestaurantRequestUpdateModel
from src.repository.category import CategoryRepo
from src.repository.restaurant.restaurant import RestaurantRepo


class RestaurantService:
    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]] = get_session) -> None:
        self.restaurant_repo = RestaurantRepo(session_getter=session_getter)
        self.cat_repo = CategoryRepo(session_getter=session_getter)


    async def create(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        update_model = await self._get_update_model(model)
        return await self.restaurant_repo.create(update_model)

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        return await self.restaurant_repo.delete(model)

    async def update(
            self,
            rest_id: int,
            model: RestaurantRequestFullModel
    ) -> None:
        update_model = await self._get_update_model(model)
        await self.restaurant_repo.update(rest_id=rest_id, model=update_model)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantDTO:
        return await self.restaurant_repo.get(model)

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantDTO]:
        return await self.restaurant_repo.get_by_owner(model)

    async def get_by_geo(
            self,
            user_id: int,
            model: Point
    ) -> list[RestaurantGeoSearch]:
        return await self.restaurant_repo.get_by_geo(model=model, user_id=user_id)

    async def get_by_geo_and_name(
            self,
            user_id: int,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        return await self.restaurant_repo.get_by_geo_and_name(model=model, user_id=user_id)

    async def get_name(self, rest_id: int) -> str:
        return await self.restaurant_repo.get_name(rest_id)

    async def get_available_properties(self, rest_id: int) -> dict[str, bool]:
        rest_properties: RestaurantRequestFullModel = await self.get(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))
        list_properties = list(RestaurantRequestFullModel.__dict__['__annotations__'].keys())
        field_status = {}
        for field in list_properties:
            value = getattr(rest_properties, field)
            field_status[field] = value is not None

        return field_status

    async def change_restaurant_property(self, rest_id: int, key: str, value: str) -> None:
        await self.restaurant_repo.change_restaurant_property(rest_id, key, value)

    async def _get_category_ids(self, category_names: List[str]) -> List[int]:
         category_ids = []
         for name in category_names:
            category_dto = CategoryDTO(name=name)
            category = await self.cat_repo.get(category_dto)
            category_ids.append(category.cat_id)
         return category_ids

    async def _get_update_model(self, model: RestaurantRequestFullModel) -> RestaurantRequestUpdateModel:
        model_data = model.model_dump()
        category_ids = await self._get_category_ids(model.categories)
        model_data['categories'] = category_ids
        return RestaurantRequestUpdateModel.model_validate(model_data, from_attributes=True)
