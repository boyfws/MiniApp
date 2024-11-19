from typing import Callable, Dict, Any, Coroutine

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status


from src.api.v1.handlers.jwt_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from src.auth import utils as auth_utils
from src.models.dto.user import UserRequest, UserGetByUserid
from src.service import get_user_service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict[str, str],
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict[str, str]) -> UserRequest:
    username: str | None = payload.get("sub")
    service = get_user_service()
    if user := await service.get_by_userid(UserGetByUserid.model_validate(username, from_attributes=True)):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str) -> Callable[[dict[str, str]], Coroutine[Any, Any, UserRequest]]:
    async def get_auth_user_from_token(
        payload: dict[str, str] = Depends(get_current_token_payload),
    ) -> UserRequest:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict[str, str] = Depends(get_current_token_payload),
    ) -> UserRequest:
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload)



get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)

get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def validate_auth_user(
    username: str = Form()
) -> UserRequest:
    un_authed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username",
    )
    service = get_user_service()
    if not (user := await service.get_by_userid(UserGetByUserid.model_validate(username, from_attributes=True))):
        return user
    raise un_authed_exc
