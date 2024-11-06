from .owner import OwnerService
from .user import UserService
from ...repository.tables.owner import OwnerRepo
from ...repository.tables.user import UserRepo


def get_user_service() -> UserService:
    return UserService(repo=UserRepo())

def get_owner_service() -> OwnerService:
    return OwnerService(repo=OwnerRepo())

__all__ = [
    'UserService', 'get_user_service',
    'OwnerService', 'get_owner_service'
]