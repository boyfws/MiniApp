from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from src.models.dto.restaurant import (RestaurantRequestUsingGeoPoint, RestaurantResponse,
                                                RestaurantResult, RestaurantRequestUsingOwner,
                                                RestaurantRequestUsingID, RestaurantRequestUsingGeoPointAndName,
                                                RestaurantRequestFullModel)
from src.models.orm.schemas import Restaurant

from src.repository.interface import TablesRepositoryInterface


class RestaurantRepo(TablesRepositoryInterface):
    def __init__(self):
        self.model: Restaurant = Restaurant()

    async def create(
            self,
            session: AsyncSession,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        return RestaurantResult()

    async def delete(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        return RestaurantResult()

    async def update(
            self,
            session: AsyncSession,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        return RestaurantResult()

    async def get(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantResponse:
        return RestaurantResponse()

    async def get_by_geo(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPoint
    ) -> RestaurantResponse:
        return RestaurantResponse()

    async def get_by_geo_and_name(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> RestaurantResponse:
        return RestaurantResponse()

    async def get_by_owner(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingOwner
    ) -> RestaurantResponse:
        return RestaurantResponse()


