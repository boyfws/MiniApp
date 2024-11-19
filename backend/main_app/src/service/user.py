from src.database.sql_session import get_session
from src.models.dto.user import UserRequest, UserResult, UserGetByUserid
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

    async def get_by_userid(
            self,
            model: UserGetByUserid
    ) -> UserRequest:
        async with get_session() as session:
            return await self.repo.get_by_username(session, model)


if __name__ == "__main__":
    import asyncio
    service = UserService(UserRepo())
    # asyncio.run(service.get_by_userid(UserGetByUserid(userid=1)))
    asyncio.run(service.create_user(UserRequest(id=465342)))
