from typing import Optional

from sqlalchemy import insert, select, exists, Row
from src.models.dto.user import UserResult, UserRequest
from src.models.orm.schemas import User
from src.repository.interface import TablesRepositoryInterface


class UserRepo(TablesRepositoryInterface):

    async def create_user(
            self,
            user_id: int,
    ) -> UserResult:
        async with self.session_getter() as session:
            await session.execute(
                insert(User).values(id=user_id)
            )
            return UserResult(status=200)

    async def is_user(self, user_id: int) -> bool:
        async with self.session_getter() as session:
            stmt = select(exists().where(User.id == user_id))
            result = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = result.first()
            if row is None:
                raise ValueError("Nothing returned from the db Users")
            return row[0]