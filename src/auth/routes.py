import logging

from fastapi import APIRouter, Depends, Response, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.exc import NoResultFound

from src.auth.dependencies import (
    validate_auth_user,
    verify_fingerprint,
    extract_refresh_token_from_cookie,
)
from src.base.base_model import User
from src.auth.schemas import AccessTokenInfo
from src.auth.services import auth_service
from exceptions import (
    LoginExist,
    EmailExist,
    UnexpectedError,
    UserEmailDoesNotExist,
    ResetTokenPasswordIncorrect,
)
from users.dependencies import (
    get_current_user_from_access_token_payload,
    get_current_user_for_refresh,
)
from users.schemas import UserSchema, UserCreate, UserRead, UserNewPassword
from users.services import user_service

logger = logging.getLogger("debug")

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login", response_model=AccessTokenInfo)
async def auth_user_issue_jwt(
    response: Response,
    user: UserSchema = Depends(validate_auth_user),
    # fingerprint: str = Depends(verify_fingerprint),
):
    fingerprint = "1"
    tokens = await auth_service.create_tokens(user=user, fingerprint=fingerprint)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)
    return AccessTokenInfo(access_token=tokens.access_token)


@router.post("/logout", status_code=200)
async def auth_user_logout(
    response: Response,
    user: UserSchema = Depends(get_current_user_from_access_token_payload),
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
    fingerprint: str = Depends(verify_fingerprint),
):
    """
    Клиентская сторона самостоятельно удаляет access_token из заголовка!
    Сервер удаляет refresh_token из куков
    """
    response.delete_cookie(key="refresh_token", httponly=True)
    try:
        await auth_service.delete_refresh_token(
            user=user, refresh_token=refresh_token_from_cookie, fingerprint=fingerprint
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token does not exist in db",
        )


@router.post("/refresh", response_model=AccessTokenInfo)
async def auth_refresh_jwt(
    response: Response,
    fingerprint: str = Depends(verify_fingerprint),
    refresh_token_from_cookie: str = Depends(extract_refresh_token_from_cookie),
    user: UserSchema = Depends(get_current_user_for_refresh),
):
    """
    Обновляет access_token. Обращаться на данный эндпоинт, когда время действия access_token
    подходит к концу или уже закончилось
    """
    try:
        logger.debug(user)
        await auth_service.delete_refresh_token(
            user=user, refresh_token=refresh_token_from_cookie, fingerprint=fingerprint
        )
    except NoResultFound:  # продумать как обработать ошибки
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # исправить
            detail="Invalid username or password",  # добавить больше ошибок
        )
    tokens = await auth_service.create_tokens(user=user, fingerprint=fingerprint)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)
    return AccessTokenInfo(access_token=tokens.access_token)


@router.post("/register", response_model=UserRead, response_model_exclude_none=True)
async def auth_register_user(
    user_data: UserCreate,
):
    try:
        created_user: User = await user_service.create_user(user_data)
        return created_user
    except LoginExist as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.message,
        )
    except EmailExist as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.message,
        )
    except UnexpectedError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex.message,
        )


@router.post("/forgot_password", status_code=200)
async def auth_forgot_password(
    email: EmailStr,
):
    """
    Принимает email пользователя, который забыл пароль. Возвращает reset_token, который нужно
    передать на эндпоинт /reset_password
    """
    try:
        reset_token = await auth_service.create_reset_token_if_forgot_password(email)
    except UserEmailDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # исправить
            detail="Invalid email",
        )

    return {"reset_token": reset_token}


@router.post(
    "/reset_password",
    status_code=200,
    responses={
        200: {"description": "Successful reset"},
        401: {"description": ResetTokenPasswordIncorrect().message},
    },
)
async def auth_reset_password(reset_token: str, new_password: UserNewPassword):
    """
    Присваивает пользователю новый пароль
    """
    try:
        await auth_service.validate_and_set_new_user_password(
            reset_token=reset_token, new_password=new_password.password
        )
    except ResetTokenPasswordIncorrect as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message)
