from src.database.sql_session import get_session
from src.models.dto.favourites import AllFavouriteCategoriesRequest, FavouriteCategoryResponse, FavouriteCategoryDTO
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.service.interface import ServiceInterface


class FavouriteCategoriesService:
    def __init__(self, repo: FavouriteCategoryRepo) -> None:
        self.repo: FavouriteCategoryRepo = repo

    async def delete(self, model: FavouriteCategoryDTO) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def create(self, model: FavouriteCategoryDTO) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.create(session, model)

    async def get_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> list[FavouriteCategoryResponse]:
        async with get_session() as session:
            return await self.repo.get_all_user_fav_categories(session, model)

    async def drop_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.drop_all_user_fav_categories(session, model)
