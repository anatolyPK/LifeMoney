import logging
import re

from sqlalchemy.exc import IntegrityError

from exceptions import LoginExist, EmailExist, UnexpectedError
from src.base.base_model import User
from core.config.database import db_helper
from src.base.sqlalchemy_repository import SqlAlchemyRepository
from users.schemas import UserCreate


logger = logging.getLogger("main")


class UserRepository(SqlAlchemyRepository):
    async def create(self, data: UserCreate) -> User:
        try:
            return await super().create(data)
        except IntegrityError as ex:
            error_message = str(ex.orig)

            match = re.search(
                r'duplicate key value violates unique constraint "([^"]+)"',
                error_message,
            )
            if match:
                constraint_name = match.group(1)
                if constraint_name == "user_username_key":
                    raise LoginExist()
                elif constraint_name == "ix_user_email":
                    raise EmailExist()
            logger.warning(f"{ex} {match} {data}")
            raise UnexpectedError()


user_repository = UserRepository(
    model=User, db_session=db_helper.get_db_session_context
)
