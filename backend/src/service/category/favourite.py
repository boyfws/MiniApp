from src.models.dto.favourites import FavouriteCategoryDTO, FavouriteCategoryRequest
from src.repository.category import CategoryRepo
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from src.repository.user import UserRepo
from src.repository.utils import create_user_if_does_not_exist


class FavouriteCategoriesService:
    def __init__(
            self,
            repo: FavouriteCategoryRepo,
            cat_repo: CategoryRepo,
            user_repo: UserRepo
    ) -> None:
        self.repo: FavouriteCategoryRepo = repo
        self.cat_repo: CategoryRepo = cat_repo
        self.user_repo: UserRepo = user_repo

    async def delete(self, model: FavouriteCategoryDTO) -> None:
        cat_id = await self.cat_repo.get(cat_name=model.cat_name)
        await self.repo.delete(FavouriteCategoryRequest(user_id=model.user_id, cat_id=cat_id))

    async def create(self, model: FavouriteCategoryDTO) -> None:
        await create_user_if_does_not_exist(user_repo=self.user_repo, user_id=model.user_id)
        cat_id = await self.cat_repo.get(cat_name=model.cat_name)
        await self.repo.create(FavouriteCategoryRequest(user_id=model.user_id, cat_id=cat_id))

    async def get_all_user_fav_categories(self, user_id: int) -> list[str]:
        cat_id_list = await self.repo.get_all_user_fav_categories(user_id)
        return [await self.cat_repo.get_name(cat_id) for cat_id in cat_id_list]

    async def drop_all_user_fav_categories(self, user_id: int) -> None:
        await self.repo.drop_all_user_fav_categories(user_id)
