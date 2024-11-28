from contextlib import _AsyncGeneratorContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql_session import get_session
from src.repository.owner import OwnerRepo


class OwnerService:

    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]]=get_session) -> None:
        self.repo = OwnerRepo(session_getter=session_getter)

    async def create_owner(
            self,
            owner_id: int
    ) -> None:
        return await self.repo.create_owner(owner_id)