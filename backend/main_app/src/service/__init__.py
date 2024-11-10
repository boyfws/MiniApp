from .user import UserService
from ..repository.user import UserRepo


def get_user_service() -> UserService:
    return UserService(repo=UserRepo())

__all__ = [
    'UserService', 'get_user_service',
]