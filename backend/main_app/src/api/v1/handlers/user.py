from fastapi import APIRouter, Depends

from src.models.dto.user import UserRequest, UserResult, UserRequestUpdate, UserGetByUsername
from src.service import get_user_service, UserService

user_router = APIRouter(
    prefix="/User",
    tags=["User"]
)

@user_router.post("/create_user/")
async def create_user(
        model: UserRequest,
        service: UserService = Depends(get_user_service)
) -> UserResult:
    return await service.create_user(model)

@user_router.put("/update_username/")
async def update_username(
        model: UserRequestUpdate,
        service: UserService = Depends(get_user_service)
) -> UserResult:
    return await service.update_username(model)

@user_router.get("/get_by_username/")
async def get_by_username(
        model: UserGetByUsername,
        service: UserService = Depends(get_user_service)
) -> UserRequest:
    return await service.get_by_username(model)
