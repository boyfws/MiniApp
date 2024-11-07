from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from src.models.dto.owner import OwnerRequest, OwnerResult, OwnerRequestUpdate
from src.models.orm.owner import Owners


class OwnerRepo:

    def __init__(self):
        self.model: Owners = Owners()

    async def create_owner(
            self,
            session: AsyncSession,
            model: OwnerRequest
    ) -> OwnerResult:
        result = await session.scalars(
            insert(self.model.__tablename__)
            .values(**{"name": model.name})
            .returning(self.model.id)
        )
        return OwnerResult.model_validate(result, from_attributes=True)

    async def update_owner_name(
            self,
            session: AsyncSession,
            model: OwnerRequestUpdate
    ) -> OwnerResult:
        result = await session.scalars(
            update(self.model.__tablename__)
            .where(self.model.name == model.old_name)
            .values(**{"name": model.new_name})
            .returning(self.model.id)
        )
        return OwnerResult.model_validate(result, from_attributes=True)
