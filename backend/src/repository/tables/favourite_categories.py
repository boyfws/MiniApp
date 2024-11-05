from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from interface import TablesRepositoryInterface
from src.models.dto.favourites import FavouriteCategoryRequest, FavouriteCategoryResponse, FavouriteRestaurantRequest, \
    FavouriteRestaurantResponse, FavouriteCategoryDTO, FavouriteRestaurantDTO, AllFavouriteCategoriesRequest, \
    AllFavouriteRestaurantsRequest
from src.models.orm.favourites.category import FavouriteCategory
from src.models.orm.favourites.restaurant import FavouriteRestaurant


class FavouriteCategoryRepo(TablesRepositoryInterface):

    def __init__(self, model: FavouriteCategory):
        self.model: FavouriteCategory = model

    async def delete(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: FavouriteCategoryRequest
    ) -> FavouriteCategoryDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.cat_id == model.cat_id)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def get_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteRestaurantDTO:
        await session.scalars(
            select(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...

    async def drop_all_user_fav_categories(
            self,
            session: AsyncSession,
            model: AllFavouriteCategoriesRequest
    ) -> FavouriteCategoryResponse:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
        )
        return ...