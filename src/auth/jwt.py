import logging

import jwt

from datetime import datetime, timezone, timedelta

from fastapi import HTTPException

from starlette import status

from src.core.config.project import settings

logger = logging.getLogger("debug")


def validate_token_type(token_type_from_payload: str, token_type: str) -> bool:
    if token_type_from_payload == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
    )


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )
        return decoded
    except jwt.InvalidTokenError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.args)


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {settings.auth_jwt.TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def extract_payload_from_token(token: str) -> dict:
    try:
        return decode_jwt(
            token=token,
        )
    except jwt.InvalidTokenError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message)
