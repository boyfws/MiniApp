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
        await session.scalars(
            insert(self.model)
            .values(**model.dict())
        )
        return ...

    async def delete(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantResult:
        await session.scalars(
            delete(self.model)
            .where(self.model.id == model.rest_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: RestaurantRequestFullModel
    ) -> RestaurantResult:
        await session.scalars(
            update(self.model)
            # TODO: сделать норм модель ресторана
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingID
    ) -> RestaurantResponse:
        await session.scalars(
            select(self.model)
            .where(self.model.id == model.rest_id)
        )
        return ...

    async def get_by_geo(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPoint
    ) -> RestaurantResponse:
        await session.scalars(
            select(self.model)
            # TODO: сделать тут как-то фильтрацию по геопозиции
        )
        return ...

    async def get_by_geo_and_name(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingGeoPointAndName
    ) -> RestaurantResponse:
        await session.scalars(
            select(self.model)
            # TODO: сделать фильтрацию через гео и паттерн названия
        )
        return ...

    async def get_by_owner(
            self,
            session: AsyncSession,
            model: RestaurantRequestUsingOwner
    ) -> RestaurantResponse:
        await session.scalars(
            select(self.model)
            .where(self.model.owner_id == model.owner_id)
        )
        return ...


