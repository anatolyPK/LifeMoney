from fastapi import HTTPException
from starlette import status

from backend.src.users.schemas import UserInfoFromPayload


async def check_user_status(
    user: UserInfoFromPayload, error_message: str, attribute: str
) -> UserInfoFromPayload:
    if getattr(user, attribute):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)
