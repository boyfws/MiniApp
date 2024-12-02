from typing import Optional

from sqlalchemy import insert, Row

from src.models.orm.schemas import Owner
from src.repository.interface import TablesRepositoryInterface


class OwnerRepo(TablesRepositoryInterface):
    async def create_owner(self, owner_id: int) -> None:
        async with self.session_getter() as session:
            stmt = insert(Owner).values(id=owner_id)
            await session.execute(stmt)