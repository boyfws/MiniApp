from src.database.sql_session import get_session
from src.models.dto.category import CategoryResult, CategoryDTO, CategoryRequestByName
from src.repository.category.category import CategoryRepo


class CategoryService:

    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def get(self, model: CategoryRequestByName) -> CategoryDTO:
        async with get_session() as session:
            return await self.repo.get(session, model)

    async def create(self, model: CategoryDTO) -> CategoryResult:
        async with get_session() as session:
            return await self.repo.create(session, model)
