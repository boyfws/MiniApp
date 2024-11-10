from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

from src.models.dto.user import UserResult, UserRequest, UserRequestUpdate, UserGetByUsername
from src.models.orm.schemas import User


class UserRepo:

    def __init__(self) -> None:
        self.model: User = User()

    async def create_user(
            self,
            session: AsyncSession,
            model: UserRequest
    ) -> UserResult:
        return UserResult()

    async def update_username(
            self,
            session: AsyncSession,
            model: UserRequestUpdate
    ) -> UserResult:
        return UserResult()

    async def get_by_username(
            self,
            session: AsyncSession,
            model: UserGetByUsername
    ) -> UserRequest:
        return UserRequest()
