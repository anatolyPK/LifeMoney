import logging

from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError

from backend.src.users.dependencies import get_current_active_user, get_current_superuser
from backend.src.users.schemas import UserRead, UserInfoFromPayload, UserUpdate, UserSchema
from backend.src.users.services import user_service

from backend.src.base.base_model import User

logger = logging.getLogger("debug")

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/me", response_model=UserRead)
async def user_check_self_info(
    user: UserInfoFromPayload = Depends(get_current_active_user),
):
    return UserRead(logged_in_at=user.iat, **user.dict())


@router.patch("/me", response_model=UserRead)
async def patch_current_user(
    new_users_data: UserUpdate,
    user: UserInfoFromPayload = Depends(get_current_active_user),
):
    updated_user: User = await user_service.update(
        pk=user.id, new_user_data=new_users_data
    )
    user_read_dict = updated_user.__dict__
    user_read_dict.update({"logged_in_at": user.iat})
    return UserRead(**user_read_dict)


@router.get("/{id}", response_model=UserRead, response_model_exclude_none=True)
async def check_user_info(
    id: str,
    user: UserInfoFromPayload = Depends(get_current_superuser),
):
    try:
        user_info: UserSchema = await user_service.get_user(id=id)
        return UserRead(**user_info.dict())
    except InvalidTokenError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.message)


@router.patch("/{id}", response_model=UserRead, response_model_exclude_none=True)
async def patch_user(
    id: str,
    new_users_data: UserUpdate,
    user: UserInfoFromPayload = Depends(get_current_superuser),
):
    updated_user: User = await user_service.update(pk=id, new_user_data=new_users_data)
    return UserRead.from_orm(updated_user)
