from .menu import MenuService
from .owner import OwnerService
from .user import UserService
from ..database.mongo_db import get_db
from ..database.sql_session import get_session
from ..repository.user import UserRepo


def get_user_service() -> UserService:
    return UserService(repo=UserRepo())

def get_owner_service() -> OwnerService:
    return OwnerService()

def get_menu_service() -> MenuService:
    return MenuService()

__all__ = [
    'UserService', 'get_user_service',
    'get_menu_service', 'MenuService',
    'get_owner_service', 'OwnerService'
]