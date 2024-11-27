from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPointAndName, \
    RestaurantGeoSearch, Point
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
            rest_id: int,
            model: RestaurantRequestFullModel
    ) -> None:
        await self.repo.update(rest_id=rest_id, model=model)

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
            model: Point
    ) -> list[RestaurantGeoSearch]:
        return await self.repo.get_by_geo(model)

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantGeoSearch]:
        return await self.repo.get_by_geo_and_name(model)
