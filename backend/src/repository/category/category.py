from typing import Optional

from src.models.dto.category import CategoryDTO, CategoryResult
from src.models.orm.schemas import Category
from sqlalchemy import select, insert, Row

from src.repository.interface import TablesRepositoryInterface


class CategoryRepo(TablesRepositoryInterface):

    async def get(
            self,
            model: CategoryDTO
    ) -> CategoryResult:
        async with self.session_getter() as session:
            stmt = select(Category.id).where(Category.name == model.name)
            cat = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = cat.first()
            if row is None:
                raise ValueError("No category ID returned from the database")
            return CategoryResult(cat_id=int(row[0]))

    async def get_name(
            self,
            cat_id: int
    ) -> str:
        async with self.session_getter() as session:
            stmt = select(Category.name).where(Category.id == cat_id)
            cat_name = await session.execute(stmt)
            row: Optional[Row[tuple[int]]] = cat_name.first()
            if row is None:
                raise ValueError("No category name returned from the databases")
            return row[0]

    async def get_all(self) -> list[CategoryDTO]:
        async with self.session_getter() as session:
            stmt = select(Category.name)
            categories = await session.execute(stmt)
            return [
                CategoryDTO.model_validate(cat, from_attributes=True) for cat in categories.all()
            ]

