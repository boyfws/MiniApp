from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, text

from src.models.dto.user import UserResult, UserRequest, UserGetByUserid
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

    async def get_by_username(
            self,
            session: AsyncSession,
            model: UserGetByUserid
    ) -> UserRequest:
        stmt = select(User.id).where(User.id == model.userid)
        response = session.execute(stmt)
        return [UserRequest.model_validate(res, from_attributes=True) for res in (await response).all()][0]
