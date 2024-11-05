from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from src.repository.tables.interface import TablesRepositoryInterface


class AddressRepo(TablesRepositoryInterface):

    def __init__(self, model: ...):
        self.model: ... = model

    async def delete(
            self,
            session: AsyncSession,
            model: ...
    ) -> ...:
        await session.scalars(
            delete(self.model.__tablename__)

        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: ...
    ) -> ...:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: ...
    ) -> ...:
        await session.scalars(
            select(self.model)
        )
        return ...