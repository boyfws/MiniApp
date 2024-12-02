from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
)
from pydantic import BaseModel

from src.api.v1.handlers.jwt_auth.helpers import (
    create_access_token,
    create_refresh_token, UserRequestMock,
)
from src.api.v1.handlers.jwt_auth.validation import (
    get_current_auth_user_for_refresh,
    validate_auth_user,
    # REFRESH_TOKEN_TYPE,
    # get_auth_user_from_token_of_type,
    # UserGetterFromToken,
)


http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


jwt_router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@jwt_router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserRequestMock = Depends(validate_auth_user),
) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@jwt_router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    # todo: validate user is active!!
    user: UserRequestMock = Depends(get_current_auth_user_for_refresh),
    # user: UserRequest = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserRequest = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
) -> TokenInfo:
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


# @router.get("/users/me/")
# async def auth_user_check_self_info(
#     payload: dict = Depends(get_current_token_payload),
#     user: UserRequest = Depends(get_current_active_auth_user),
# ):
#     iat = payload.get("iat")
#     return {
#         "username": user.name,
#         "is_owner": user.is_owner,
#         "logged_in_at": iat,
#     }
