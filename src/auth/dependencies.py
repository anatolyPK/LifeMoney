import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Header, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from src.auth.jwt import extract_payload_from_token
from src.core.security import validate_password
from src.exceptions import InvalidSalt
from src.users.schemas import UserInfoFromPayload
from src.users.services import user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


logger_debug = logging.getLogger("debug")
logger_main = logging.getLogger("main")


async def verify_fingerprint(x_device_fingerprint: str = Header(None)):
    if x_device_fingerprint is None:
        raise HTTPException(status_code=400, detail="Fingerprint header is missing")
    return x_device_fingerprint


async def extract_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")
    return refresh_token


async def validate_auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )

    if not (user := await user_service.get_user(email=form_data.username)):
        raise unauthed_exc

    try:
        if not validate_password(
            password=form_data.password, hashed_password=user.hashed_password
        ):
            raise unauthed_exc
    except InvalidSalt:
        logger_main.warning(
            f"Invalid salt! User: {user.__dict__} \n "
            f"Form data: {form_data.__dict__}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Already fixing"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User inactive"
        )
    return user


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserInfoFromPayload:
    payload = extract_payload_from_token(token)
    return UserInfoFromPayload(
        token_type=payload.get("type"), id=payload.get("sub"), **payload
    )
