from .category import CategoryService

def get_category_service() -> CategoryService:
    return CategoryService()

__all__ = ["CategoryService", "get_category_service"]
