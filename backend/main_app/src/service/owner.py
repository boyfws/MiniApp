from src.database.sql_session import get_session
from src.models.dto.owner import OwnerRequestUpdate, OwnerResult, OwnerRequest
from src.repository.owner import OwnerRepo


class OwnerService:

    def __init__(self, repo: OwnerRepo):
        self.repo = repo

    async def create_owner(
            self,
            model: OwnerRequest
    ) -> OwnerResult:
        async with get_session() as session:
            return await self.repo.create_owner(session, model)

    async def update_owner_name(
            self,
            model: OwnerRequestUpdate
    ) -> OwnerResult:
        async with get_session() as session:
            return await self.repo.update_owner_name(session, model)