from src.models.dto.category import CategoryResult, CategoryDTO, CategoryRequestByName
from src.repository.category.category import CategoryRepo


class CategoryService:

    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def get(self, model: CategoryRequestByName) -> CategoryDTO:
        return await self.repo.get(model)

    async def create(self, model: CategoryDTO) -> CategoryResult:
        return await self.repo.create(model)
