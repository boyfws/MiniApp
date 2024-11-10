from src.models.dto.category import CategoryRequest, CategoryDTO, CategoryResult, CategoryRequestUpdate
from src.models.orm.schemas import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from src.repository.interface import TablesRepositoryInterface


class CategoryRepo(TablesRepositoryInterface):

    def __init__(self) -> None:
        self.model: Category = Category()

    async def delete(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryResult:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.name == model.name)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: CategoryRequestUpdate
    ) -> CategoryResult:
        await session.scalars(
            update(self.model.__tablename__)
            .where(self.model.name == model.old_name)
            .values(**{"name": model.new_name})
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryDTO:
        await session.scalars(
            select(self.model.__tablename__)
            .where(self.model.id == model.cat_id)
            .where(self.model.name == model.name)
        )
        return ...

    async def create(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryResult:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...
