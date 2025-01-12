from src.repository.category.category import CategoryRepo
from src.repository.category.favourite_categories import FavouriteCategoryRepo
from .category import CategoryService
from .favourite import FavouriteCategoriesService
from ...repository.user import UserRepo


def get_category_service() -> CategoryService:
    return CategoryService(repo=CategoryRepo())

def get_fav_category_service() -> FavouriteCategoriesService:
    return FavouriteCategoriesService(
        repo=FavouriteCategoryRepo(),
        user_repo=UserRepo(),
        cat_repo=CategoryRepo()
    )

__all__ = [
    "CategoryService", "get_category_service",
    "FavouriteCategoriesService", "get_fav_category_service"
]
