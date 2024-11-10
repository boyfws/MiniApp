from src.database.sql_session import get_session
from src.models.dto.category import CategoryResult, CategoryRequestUpdate, CategoryRequest, CategoryDTO
from src.repository.category.category import CategoryRepo
from src.service.interface import ServiceInterface


class CategoryService:

    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def delete(self, model: CategoryRequest) -> CategoryResult:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def update(self, model: CategoryRequestUpdate) -> CategoryResult:
        async with get_session() as session:
            return await self.repo.update(model=model, session=session)

    async def get(self, model: CategoryRequest) -> CategoryDTO:
        async with get_session() as session:
            return await self.repo.get(session, model)

    async def create(self, model: CategoryRequest) -> CategoryResult:
        async with get_session() as session:
            return await self.repo.create(session, model)
