import uuid


from backend.src.auth.schemas import NewUserPassword
from backend.src.core.security import hash_password
from backend.src.users.repository import user_repository
from backend.src.users.schemas import (
    UserUpdate,
    UserUpdateWithHashedPassword,
    UserSchema,
    UserCreate,
    UserCreateSchemeForDB,
)

from backend.src.base.base_model import User
from backend.src.base.base_service import BaseService
from backend.src.exceptions import MissUserIdOrEmail
from backend.src.utils.email import EmailSender


class UserService(BaseService):
    async def update(self, pk: uuid.UUID, new_user_data: UserUpdate) -> User:
        hashed_password = None
        if new_user_data.password is not None:
            hashed_password = hash_password(new_user_data.password).decode()
        updated_date = UserUpdateWithHashedPassword(
            **new_user_data.dict(), hashed_password=hashed_password
        )
        return await self.repository.update(updated_date, id=pk)

    async def set_new_user_password(self, user: UserSchema, new_password: str):
        hashed_password = hash_password(new_password).decode()
        update_data = NewUserPassword(hashed_password=str(hashed_password))
        await self.repository.update(update_data, id=user.id)

    async def get_user(self, email: str = None, id: str = None) -> UserSchema:
        if email and (user := await self.repository.get_single(email=email)):
            return UserSchema.from_orm(user)
        elif id and (user := await self.repository.get_single(id=id)):
            return UserSchema.from_orm(user)
        else:
            raise MissUserIdOrEmail()

    async def create_user(self, user_data: UserCreate) -> User:
        users_data_for_db = self._convert_model_in_db_models(user_data)
        created_user = await self.repository.create(users_data_for_db)
        await EmailSender.send(user_data)
        return created_user

    @staticmethod
    def _convert_model_in_db_models(user_data: UserCreate) -> UserCreateSchemeForDB:
        user_data_dict = user_data.dict()
        user_password = user_data_dict.pop("password")
        user_hashed_password = hash_password(user_password).decode()
        return UserCreateSchemeForDB(
            **user_data_dict, hashed_password=user_hashed_password
        )


user_service = UserService(user_repository)
