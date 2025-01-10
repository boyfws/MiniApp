from src.models.dto.favourites import FavouriteCategoryDTO
from src.repository.category.favourite_categories import FavouriteCategoryRepo

class FavouriteCategoriesService:
    def __init__(self, repo: FavouriteCategoryRepo) -> None:
        self.repo: FavouriteCategoryRepo = repo

    async def delete(self, model: FavouriteCategoryDTO) -> None:
        await self.repo.delete(model)

    async def create(self, model: FavouriteCategoryDTO) -> None:
        await self.repo.create(model)

    async def get_all_user_fav_categories(self, user_id: int) -> list[str]:
        return await self.repo.get_all_user_fav_categories(user_id)

    async def drop_all_user_fav_categories(self, user_id: int) -> None:
        await self.repo.drop_all_user_fav_categories(user_id)
