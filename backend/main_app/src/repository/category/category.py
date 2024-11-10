from src.models.dto.category import CategoryRequest, CategoryDTO, CategoryResult, CategoryRequestUpdate
from src.models.orm.schemas import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from src.repository.interface import TablesRepositoryInterface


class CategoryRepo:

    def __init__(self) -> None:
        self.model: Category = Category()

    async def delete(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryResult:
        return CategoryResult()

    async def update(
            self,
            session: AsyncSession,
            model: CategoryRequestUpdate
    ) -> CategoryResult:
        return CategoryResult()

    async def get(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryDTO:
        return CategoryDTO()

    async def create(
            self,
            session: AsyncSession,
            model: CategoryRequest
    ) -> CategoryResult:
        return CategoryResult()
