from sqlalchemy import insert, update, select, text

from src.database.sql_session import get_session
from src.models.dto.user import UserResult, UserRequest, UserGetByUserid
from src.models.orm.schemas import User


class UserRepo:

    async def create_user(
            self,
            model: UserRequest
    ) -> UserResult:
        async with get_session() as session:
            await session.execute(
                insert(User).values(**model.dict())
            )
            return UserResult(status=200)

    async def get_by_username(
            self,
            model: UserGetByUserid
    ) -> UserRequest:
        async with get_session() as session:
            stmt = select(User.id).where(User.id == model.userid)
            response = session.execute(stmt)
            return [UserRequest.model_validate(res, from_attributes=True) for res in (await response).all()][0]
