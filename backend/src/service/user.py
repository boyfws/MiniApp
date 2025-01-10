from src.repository.user import UserRepo


class UserService:

    def __init__(self, repo: UserRepo):
        self.repo = repo