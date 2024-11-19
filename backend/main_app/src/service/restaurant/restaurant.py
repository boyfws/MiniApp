from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPoint, RestaurantRequestUsingGeoPointAndName
from src.repository.restaurant.restaurant import RestaurantRepo


class RestaurantService:
    def __init__(self) -> None:
        self.repo = RestaurantRepo()
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
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        return await self.repo.update(model)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestFullModel:
        return await self.repo.get(model)

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
        return await self.repo.get_by_owner(model)

    async def get_by_geo(
            self,
            model: RestaurantRequestUsingGeoPoint
    ) -> list[RestaurantRequestFullModel]:
        return await self.repo.get_by_geo(model)

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantRequestFullModel]:
        return await self.repo.get_by_geo_and_name(model)
