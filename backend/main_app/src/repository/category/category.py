from src.models.dto.category import CategoryDTO, CategoryResult
from src.models.orm.schemas import Category
from sqlalchemy import select, insert

from src.repository.interface import TablesRepositoryInterface


class CategoryRepo(TablesRepositoryInterface):

    async def get(
            self,
            model: CategoryDTO
    ) -> CategoryResult:
        async with self.session_getter() as session:
            stmt = select(Category.id).where(Category.name == model.name)
            cat = await session.execute(stmt)
            return CategoryResult(cat_id=int(cat.first()[0]))

    async def create(
            self,
            model: CategoryDTO
    ) -> CategoryResult:
        async with self.session_getter() as session:
            stmt = insert(Category).values(name=model.name).returning(Category.id)
            cat_id = await session.execute(stmt)
            return CategoryResult(cat_id=int(cat_id.first()[0]))
