from src.database.sql_session import get_session
from src.repository.owner import OwnerRepo


class OwnerService:

    def __init__(self, session_getter=get_session):
        self.repo = OwnerRepo(session_getter=session_getter)

    async def create_owner(
            self,
            owner_id: int
    ) -> None:
        return await self.repo.create_owner(owner_id)