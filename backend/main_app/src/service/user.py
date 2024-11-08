from src.database.sql_session import get_session
from src.models.dto.user import UserRequest, UserResult, UserRequestUpdate, UserGetByUsername
from src.repository.user import UserRepo


class UserService:

    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def create_user(
            self,
            model: UserRequest
    ) -> UserResult:
        async with get_session() as session:
            return await self.repo.create_user(session, model)

    async def update_username(
            self,
            model: UserRequestUpdate
    ) -> UserResult:
        async with get_session() as session:
            return await self.repo.update_username(session, model)

    async def get_by_username(
            self,
            model: UserGetByUsername
    ) -> UserRequest:
        async with get_session() as session:
            return await self.repo.get_by_username(session, model)

