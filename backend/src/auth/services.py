import logging
import uuid
from datetime import timedelta

from pydantic import EmailStr

from backend.src.auth.jwt import create_jwt, extract_payload_from_token, validate_token_type
from backend.src.auth.repository import auth_repository
from backend.src.auth.schemas import AccessAndRefreshTokens, RefreshTokenCreate
from backend.src.base.base_service import BaseService
from backend.src.core.config.project import settings
from backend.src.exceptions import UserEmailDoesNotExist, ResetTokenPasswordIncorrect
from backend.src.users.schemas import UserInfoFromPayload, UserSchema
from backend.src.users.services import user_service

logger = logging.getLogger("debug")


class TokenManager(BaseService):
    async def create_tokens(
        self, user: UserSchema | UserInfoFromPayload, fingerprint: str
    ) -> AccessAndRefreshTokens:
        access_token: str = self._create_access_token(user)
        refresh_token: str = await self._create_refresh_token(user, fingerprint)
        return AccessAndRefreshTokens(
            access_token=access_token, refresh_token=refresh_token
        )

    def _create_access_token(self, user: UserSchema | UserInfoFromPayload) -> str:
        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
        }
        return create_jwt(
            token_type=settings.auth_jwt.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    async def _create_refresh_token(
        self,
        user: UserSchema | UserInfoFromPayload,
        fingerprint: str,
    ) -> str:
        jwt_payload = {
            "sub": str(user.id),
        }
        refresh_token = create_jwt(
            token_type=settings.auth_jwt.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(
                days=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        await self._put_refresh_token(
            user_data=user, refresh_token=refresh_token, fingerprint=fingerprint
        )
        return refresh_token

    async def create_reset_token_if_forgot_password(self, email: EmailStr):
        if not (user := await user_service.get_user(email=email)):
            raise UserEmailDoesNotExist

        reset_token: str = await self._create_reset_token(user=user)
        #     send email with http reset-password and reset-token
        return reset_token

    async def _create_reset_token(
        self,
        user: UserSchema,
    ) -> str:
        jwt_payload = {
            "sub": str(user.id),
            "hashed_password": user.hashed_password,
        }

        reset_token = create_jwt(
            token_type=settings.auth_jwt.RESET_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=settings.auth_jwt.RESET_TOKEN_EXPIRE_MINUTES,
        )
        return reset_token

    async def _put_refresh_token(
        self, user_data: UserSchema, refresh_token: str, fingerprint: str
    ):
        refresh_token_dto = RefreshTokenCreate(
            user_id=user_data.id,
            refresh_token=refresh_token,
            fingerprint=fingerprint,
            should_deleted_at=None,
        )
        await self.repository.put_or_refresh_refresh_token(refresh_token_dto)

    async def delete_refresh_token(
        self, user: UserSchema, refresh_token: str, fingerprint: str
    ):
        """
        При запросе к БД проверяет, что RT и FP принадлжат данному пользователю
        """
        await self.repository.delete(
            user_id=user.id, refresh_token=refresh_token, fingerprint=fingerprint
        )


class AuthService(TokenManager):
    async def validate_and_set_new_user_password(
        self, reset_token: str, new_password: str
    ):
        user = await self._validate_reset_token_and_get_user(reset_token=reset_token)
        await user_service.set_new_user_password(user=user, new_password=new_password)

    async def _validate_reset_token_and_get_user(self, reset_token: str) -> UserSchema:
        payload = extract_payload_from_token(reset_token)
        validate_token_type(
            token_type_from_payload=payload.get("type"),
            token_type=settings.auth_jwt.RESET_TOKEN_TYPE,
        )
        user = await self._validate_token_password_and_get_user(
            password_from_payload=payload.get("hashed_password"),
            user_id=payload.get("sub"),
        )
        return user

    async def _validate_token_password_and_get_user(
        self, password_from_payload: str, user_id: uuid.UUID
    ) -> UserSchema:
        user: UserSchema = await user_service.get_user(id=user_id)
        if password_from_payload == user.hashed_password:
            return user
        raise ResetTokenPasswordIncorrect


auth_service: AuthService = AuthService(auth_repository)
