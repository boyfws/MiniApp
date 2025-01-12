from src.models.dto.favourites import FavouriteRestaurantDTO
from src.repository.restaurant.favourite_restaurants import FavouriteRestaurantRepo
from src.repository.user import UserRepo
from src.repository.utils import create_user_if_does_not_exist


class FavouriteRestaurantService:
    def __init__(self, repo: FavouriteRestaurantRepo, user_repo: UserRepo):
        self.repo = repo
        self.user_repo = user_repo
    async def delete(self, model: FavouriteRestaurantDTO) -> None:
        await self.repo.delete(model)

    async def create(self, model: FavouriteRestaurantDTO) -> int:
        await create_user_if_does_not_exist(user_repo=self.user_repo, user_id=model.user_id)
        return await self.repo.create(model)

    async def get_all_user_fav_restaurants(
            self,
            user_id: int
    ) -> list[int]:
        return await self.repo.get_all_user_fav_restaurants(user_id)

    async def drop_all_user_fav_restaurants(
            self,
            user_id: int
    ) -> None:
        return await self.repo.drop_all_user_fav_restaurants(user_id)

    async def is_favourite(self, user_id: int, rest_id: int) -> bool:
        await create_user_if_does_not_exist(user_repo=self.user_repo, user_id=user_id)
        return await self.repo.is_favourite(user_id, rest_id)