from src.models.dto.category import CategoryRequestByName, CategoryDTO, CategoryResult
from src.models.orm.schemas import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert


class CategoryRepo:

    async def get(
            self,
            session: AsyncSession,
            model: CategoryRequestByName
    ) -> CategoryDTO:
        stmt = select(Category.id, Category.name).where(Category.name == model.name)
        cat = await session.execute(stmt)
        return CategoryDTO.model_validate(cat, from_attributes=True)

    async def create(
            self,
            session: AsyncSession,
            model: CategoryDTO
    ) -> CategoryResult:
        stmt = insert(Category).values(**model.dict()).returning(Category.id)
        cat_id = await session.execute(stmt)
        return CategoryResult.model_validate(cat_id, from_attributes=True)
