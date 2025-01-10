from contextlib import _AsyncGeneratorContextManager
from typing import Callable, List, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql_session import get_session
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPointAndName, \
    RestaurantGeoSearch, Point, RestaurantDTO, RestaurantRequestUpdateModel, GeoSearchResult
from src.repository.category import CategoryRepo
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.restaurant.restaurant import RestaurantRepo


class RestaurantService:
    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]] = get_session) -> None:
        self.restaurant_repo = RestaurantRepo(session_getter=session_getter)
        self.cat_repo = CategoryRepo(session_getter=session_getter)
        self.fav_rest_repo = FavouriteRestaurantRepo(session_getter=session_getter)


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
        data_from_repo = await self.restaurant_repo.get(model)
        return RestaurantDTO.model_validate(
            await self._get_transformed_select_result_for_user(data_from_repo, model),
            from_attributes=True
        )

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
        data_from_repo = await self.restaurant_repo.get_by_owner(model)
        return [
            RestaurantRequestFullModel.model_validate(
                await self._get_full_model(item),
                from_attributes=True
            ) for item in data_from_repo
        ]

    async def get_by_geo(
            self,
            user_id: int,
            model: Point
    ) -> list[RestaurantGeoSearch]:
        data_from_repo = await self.restaurant_repo.get_by_geo(model=model)
        return [
            RestaurantGeoSearch.model_validate(
                await self._get_transformed_search_result(data, user_id),
                from_attributes=True
            ) for data in data_from_repo
        ]

    async def get_by_geo_and_name(
            self,
            user_id: int,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        data_from_repo = await self.restaurant_repo.get_by_geo_and_name(model=model)
        return [
            RestaurantGeoSearch.model_validate(
                await self._get_transformed_search_result(data, user_id),
                from_attributes=True
            ) for data in data_from_repo
        ]

    async def get_name(self, rest_id: int) -> str:
        return await self.restaurant_repo.get_name(rest_id)

    async def get_available_properties(self, rest_id: int) -> dict[str, bool]:
        rest_properties = await self.restaurant_repo.get(RestaurantRequestUsingID(rest_id=rest_id, user_id=1))
        list_properties = list(RestaurantRequestUpdateModel.model_fields.keys())
        field_status = {}
        for field in list_properties:
            value = getattr(rest_properties, field)
            field_status[field] = value is not None

        return field_status

    async def change_restaurant_property(self, rest_id: int, key: str, value: Any) -> None:
        await self.restaurant_repo.change_restaurant_property(rest_id, key, value)

    async def _get_category_ids(self, category_names: List[str]) -> List[int]:
         category_ids = []
         for name in category_names:
            category = await self.cat_repo.get(name)
            category_ids.append(category)
         return category_ids

    async def _get_category_names(self, category_ids: List[int]) -> List[str]:
        category_names = []
        for num in category_ids:
            name = await self.cat_repo.get_name(int(num))
            category_names.append(name)
        return category_names

    async def _get_update_model(self, model: RestaurantRequestFullModel) -> RestaurantRequestUpdateModel:
        model_data = model.model_dump()
        category_ids = await self._get_category_ids(model.categories)
        model_data['categories'] = category_ids
        return RestaurantRequestUpdateModel.model_validate(model_data, from_attributes=True)

    async def _get_transformed_search_result(self, model: GeoSearchResult, user_id: int) -> RestaurantGeoSearch:
        return RestaurantGeoSearch(
            id=model.id,
            name=model.name,
            main_photo=model.main_photo,
            distance=round(model.distance / 1000, 2),
            favourite_flag=await self.fav_rest_repo.is_favourite(user_id=user_id, rest_id=model.id),
            category=await self._get_category_names(model.category),
            rating=model.rating
        )

    async def _get_transformed_select_result_for_user(
            self,
            data_from_repo: RestaurantRequestUpdateModel,
            model: RestaurantRequestUsingID
    ) -> dict[str, Any]:
        data = data_from_repo.model_dump()
        data['favourite_flag'] = await self.fav_rest_repo.is_favourite(model.rest_id, model.user_id)
        data['categories'] = await self._get_category_names(data_from_repo.categories)
        return data

    async def _get_full_model(
            self,
            data_from_repo: RestaurantRequestUpdateModel
    ) -> dict[str, Any]:
        data = data_from_repo.model_dump()
        data['categories'] = await self._get_category_names(data_from_repo.categories)
        return data