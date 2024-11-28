from .menu import MenuService
from .user import UserService
from ..database.mongo_db import get_db
from ..repository.user import UserRepo


def get_user_service() -> UserService:
    return UserService(repo=UserRepo())

def get_owner_service(): ...

def get_menu_service(session_getter=get_db) -> MenuService:
    return MenuService(session_getter=session_getter)

__all__ = [
    'UserService', 'get_user_service',
    'get_menu_service', 'MenuService',
    'get_owner_service'
]