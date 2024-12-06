import hashlib

from fastapi import (
    APIRouter,
    Depends, HTTPException,
)
from fastapi.security import (
    HTTPBearer,
)
from pydantic import BaseModel
from starlette import status

from src.api.v1.handlers.jwt_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from src.auth.utils import is_valid_telegram_request

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
async def auth_user_jwt(
    data_check_string: str,
) -> TokenInfo:
    if not is_valid_telegram_request(data_check_string):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Telegram request signature.",
        )

    access_token = create_access_token(data_check_string)
    refresh_token = create_refresh_token(data_check_string)
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
    data_check_string: str,
) -> TokenInfo:
    access_token = create_access_token(data_check_string)
    return TokenInfo(
        access_token=access_token,
    )
