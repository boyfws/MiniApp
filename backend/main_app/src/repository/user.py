from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

from src.models.dto.user import UserResult, UserRequest, UserRequestUpdate, UserGetByUsername
from src.models.orm.schemas import User


class UserRepo:

    async def create_user(
            self,
            session: AsyncSession,
            model: UserRequest
    ) -> UserResult:
        await session.execute(
            insert(User).values(**model.dict())
        )
        return UserResult(status=200)

    async def update_username(
            self,
            session: AsyncSession,
            model: UserRequestUpdate
    ) -> UserResult:
        await session.execute(
            update(User).where(User.name == model.old_name).values(name=model.new_name)
        )
        return UserResult(status=200)

    async def get_by_username(
            self,
            session: AsyncSession,
            model: UserGetByUsername
    ) -> UserRequest:
        stmt = select(User.id, User.name, User.owner).where(User.name == model.username)
        response = await session.execute(stmt)
        return UserRequest.model_validate(response, from_attributes=True)
