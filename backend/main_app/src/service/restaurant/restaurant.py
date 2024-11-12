from src.database.sql_session import get_session
from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPoint, RestaurantResponse, \
    RestaurantRequestUsingGeoPointAndName
from src.repository.restaurant.restaurant import RestaurantRepo


class RestaurantService:
    def __init__(self) -> None:
        self.repo = RestaurantRepo()
    async def create(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        async with get_session() as session:
            return await self.repo.create(session, model)

    async def delete(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def update(
            self,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        async with get_session() as session:
            return await self.repo.update(session, model)

    async def get(
            self,
            model: RestaurantRequestUsingID
    ) -> RestaurantRequestFullModel:
        async with get_session() as session:
            return await self.repo.get(session, model)

    async def get_by_owner(
            self,
            model: RestaurantRequestUsingOwner
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            return await self.repo.get_by_owner(session, model)

    async def get_by_geo(
            self,
            model: RestaurantRequestUsingGeoPoint
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            return await self.repo.get_by_geo(session, model)

    async def get_by_geo_and_name(
            self,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> list[RestaurantRequestFullModel]:
        async with get_session() as session:
            return await self.repo.get_by_geo_and_name(session, model)
