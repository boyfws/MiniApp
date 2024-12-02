from sqlalchemy import insert
from src.models.dto.user import UserResult, UserRequest
from src.models.orm.schemas import User
from src.repository.interface import TablesRepositoryInterface


class UserRepo(TablesRepositoryInterface):

    async def create_user(
            self,
            model: UserRequest,
    ) -> UserResult:
        async with self.session_getter() as session:
            await session.execute(
                insert(User).values(**model.dict())
            )
            return UserResult(status=200)
