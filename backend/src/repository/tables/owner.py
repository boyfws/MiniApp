from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from src.models.dto.owner import OwnerDTO, OwnerResult
from src.models.orm.owner import Owner
from src.repository.tables.interface import TablesRepositoryInterface


class OwnerRepo(TablesRepositoryInterface):

    def __init__(self, model: Owner):
        self.model: Owner = model

    async def delete(
            self,
            session: AsyncSession,
            model: OwnerDTO
    ) -> OwnerResult:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.id == model.owner_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: OwnerDTO
    ) -> OwnerResult:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: OwnerDTO
    ) -> OwnerDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.id == model.user_id)
        )
        return ...
