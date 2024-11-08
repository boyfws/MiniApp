from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

from src.models.dto.user import UserResult, UserRequest, UserRequestUpdate, UserGetByUsername
from src.models.orm.user import Users


class UserRepo:

    def __init__(self):
        self.model: Users = Users()

    async def create_user(
            self,
            session: AsyncSession,
            model: UserRequest
    ) -> UserResult:
        result = await session.scalars(
            insert(self.model.__tablename__)
            .values(**{"name": model.name})
            .returning(self.model.id)
        )
        return UserResult.model_validate(result, from_attributes=True)

    async def update_username(
            self,
            session: AsyncSession,
            model: UserRequestUpdate
    ) -> UserResult:
        result = await session.scalars(
            update(self.model.__tablename__)
            .where(self.model.name == model.old_name)
            .values(**{"name": model.new_name})
            .returning(self.model.id)
        )
        return UserResult.model_validate(result, from_attributes=True)

    async def get_by_username(
            self,
            session: AsyncSession,
            model: UserGetByUsername
    ) -> UserRequest:
        result = await session.scalars(
            select(self.model.__tablename__)
            .where(self.model.name == model.username)
        )
        return UserRequest.model_validate(result, from_attributes=True)
