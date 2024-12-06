from fastapi import APIRouter, Depends

from src.models.dto.user import UserRequest, UserResult
from src.repository.user import UserRepo
from src.service import get_user_service, UserService
from tests.sql_connector import get_session_test

user_router = APIRouter(
    prefix="/User",
    tags=["User"]
)

def get_test_user_service() -> UserService:
    return UserService(repo=UserRepo(session_getter=get_session_test))

# @user_router.post("/create_user/")
# async def create_user(
#         model: UserRequest,
#         service: UserService = Depends(get_test_user_service)
# ) -> UserResult:
#     return await service.create_user(model)
