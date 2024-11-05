from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from src.models.dto.user import UserDTO, UserResult
from src.models.orm.user import User
from src.repository.tables.interface import TablesRepositoryInterface


class UserRepo(TablesRepositoryInterface):

    def __init__(self, model: User):
        self.model: User = model

    async def delete(
            self,
            session: AsyncSession,
            model: UserDTO
    ) -> UserResult:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.id == model.user_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: UserDTO
    ) -> UserResult:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: UserDTO
    ) -> UserDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.id == model.user_id)
        )
        return ...
