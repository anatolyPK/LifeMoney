from fastapi import APIRouter, Depends

from src.auth.manager import fastapi_users, auth_backend, current_active_user, get_user_manager
from src.models.auth import User
from src.schemas.auth import UserRead, UserCreate, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")  # Убедитесь, что у вас есть папка templates с HTML-файлами.


@router.get("/auth/verify", tags=['auth'])
async def verify_from_email(request: Request, token: str):
    return templates.TemplateResponse("verify.html", {"request": request, "token": token})

