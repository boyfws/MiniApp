from .user import UserService
from ...repository.tables.user import UserRepo


def get_user_service() -> UserService:
    return UserService(repo=UserRepo())

__all__ = [
    'UserService', 'get_user_service'
]