from src.database.sql_session import get_session
from src.models.dto.favourites import AllFavouriteCategoriesRequest, FavouriteRestaurantDTO, FavouriteCategoryResponse, \
    FavouriteCategoryRequest, FavouriteCategoryDTO
from src.repository.tables.favourite_categories import FavouriteCategoryRepo
from src.service.tables.interface import ServiceInterface, AbstractModel

class FavouriteCategoriesService(ServiceInterface):
    def __init__(self, repo: FavouriteCategoryRepo):
        self.repo = repo
    async def delete(self, model: FavouriteCategoryRequest) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def update(self, model: FavouriteCategoryRequest) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.update(session, model)

    async def get(self, model: FavouriteCategoryRequest) -> FavouriteCategoryDTO:
        async with get_session() as session:
            return await self.repo.get(session, model)

    async def get_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryDTO:
        async with get_session() as session:
            return await self.repo.get_all_user_fav_categories(session, model)

    async def drop_all_user_fav_categories(
            self,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        async with get_session() as session:
            return await self.repo.drop_all_user_fav_categories(session, model)
