import uuid
from datetime import datetime, timezone, timedelta

from pydantic import BaseModel, field_validator

from backend.src.core.config.project import settings


class NewUserPassword(BaseModel):
    hashed_password: str


class ResetTokenInfo(BaseModel):
    id: uuid.UUID
    hashed_password: str
    aud: str
    token_type: str


class AccessAndRefreshTokens(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class RefreshTokenCreate(BaseModel):
    user_id: uuid.UUID
    refresh_token: str
    fingerprint: str

    should_deleted_at: datetime | None

    @field_validator("should_deleted_at")
    @classmethod
    def set_should_deleted_at(cls, v):
        if v is None:
            REFRESH_TOKEN_EXPIRE_DAYS = settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS
            now = datetime.now(timezone.utc)
            expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            return expire.replace(tzinfo=None)
        return v
