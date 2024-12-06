import hmac
import hashlib
import urllib.parse
from datetime import datetime, timedelta
from typing import Any
import jwt

from src.config import configuration as settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict[str, Any]:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

def is_valid_telegram_request(data_check_string: str) -> bool:
    try:
        params = urllib.parse.parse_qs(data_check_string)
        hash_from_telegram = params['hash'][0]
        secret_key = hmac.new(settings.auth_jwt.bot_token.encode('utf-8'), b'WebAppData', hashlib.sha256).digest()
        computed_hash = hmac.new(data_check_string.encode('utf-8'), secret_key, hashlib.sha256).hexdigest()
        return computed_hash == hash_from_telegram
    except (KeyError, IndexError):
        return False
