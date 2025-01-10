from src.repository.category.category import CategoryRepo


class CategoryService:

    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def get(self, cat_name: str) -> int:
        return await self.repo.get(cat_name)

    async def get_all(self) -> list[str]:
        return await self.repo.get_all()
