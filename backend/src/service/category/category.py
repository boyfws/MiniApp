from src.models.dto.category import CategoryResult, CategoryDTO
from src.repository.category.category import CategoryRepo


class CategoryService:

    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def get(self, model: CategoryDTO) -> CategoryResult:
        return await self.repo.get(model)

    async def get_all(self) -> list[CategoryDTO]:
        return await self.repo.get_all()
