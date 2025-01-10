from src.models.orm.schemas import Category
from sqlalchemy import select

from src.repository.interface import TablesRepositoryInterface
from src.repository.utils import _execute_and_fetch_first


class CategoryRepo(TablesRepositoryInterface):

    async def get(self, cat_name: str) -> int:
        async with self.session_getter() as session:
            stmt = select(Category.id).where(Category.name == cat_name)
            row = await _execute_and_fetch_first(session, stmt,"No category found")
            return int(row[0])

    async def get_name(self, cat_id: int) -> str:
        async with self.session_getter() as session:
            stmt = select(Category.name).where(Category.id == cat_id)
            row = await _execute_and_fetch_first(session, stmt, "No category name found")
            return row[0]

    async def get_all(self) -> list[str]:
        async with self.session_getter() as session:
            stmt = select(Category.name)
            categories = await session.execute(stmt)
            return [cat[0] for cat in categories.all()]

