from typing import Optional

from sqlalchemy import insert, Row, select, exists

from src.models.orm.schemas import Owner
from src.repository.interface import TablesRepositoryInterface


class OwnerRepo(TablesRepositoryInterface):
    async def create_owner(self, owner_id: int) -> None:
        async with self.session_getter() as session:
            stmt = insert(Owner).values(id=owner_id)
            await session.execute(stmt)

    async def is_owner(self, owner_id: int) -> bool:
        async with self.session_getter() as session:
            stmt = select(exists().where(Owner.id == owner_id))
            result = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = result.first()
            if row is None:
                raise ValueError("Nothing returned from the db")
            return row[0]