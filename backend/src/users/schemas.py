import uuid

from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserSchema(BaseUserSchema):
    hashed_password: str  # ставить что-то одно и

    class Config:
        strict = True
        from_attributes = True


class UserRead(BaseUserSchema):
    logged_in_at: int | None = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateSchemeForDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int = 2
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdateWithHashedPassword(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None


class UserInfoFromPayload(BaseModel):
    token_type: str
    id: uuid.UUID
    exp: int
    iat: int
    username: str = None
    email: EmailStr = None
    is_superuser: bool = None
    is_verified: bool = None
    is_active: bool = None


class UserNewPassword(BaseModel):
    password: str
