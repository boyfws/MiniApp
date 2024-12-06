from src.models.dto.user import UserRequest, UserResult
from src.repository.user import UserRepo


class UserService:

    def __init__(self, repo: UserRepo):
        self.repo = repo

    # async def create_user(
    #         self,
    #         model: UserRequest
    # ) -> UserResult:
    #     return await self.repo.create_user(model)
