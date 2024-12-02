from src.models.dto.favourites import AllFavouriteCategoriesRequest, FavouriteCategoryResponse, FavouriteCategoryDTO
from src.repository.category.favourite_categories import FavouriteCategoryRepo

class FavouriteCategoriesService:
    def __init__(self, repo: FavouriteCategoryRepo) -> None:
        self.repo: FavouriteCategoryRepo = repo

    async def delete(self, model: FavouriteCategoryDTO) -> FavouriteCategoryResponse:
        return await self.repo.delete(model)

    async def create(self, model: FavouriteCategoryDTO) -> FavouriteCategoryResponse:
        return await self.repo.create(model)

    async def get_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> list[FavouriteCategoryResponse]:
        return await self.repo.get_all_user_fav_categories(model)

    async def drop_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> AllFavouriteCategoriesRequest:
        return await self.repo.drop_all_user_fav_categories(model)
