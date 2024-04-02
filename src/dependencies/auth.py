from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db.database import db_helper
from src.models.auth import User


async def get_user_db(session: AsyncSession = Depends(db_helper.get_db_session)):
    yield SQLAlchemyUserDatabase(session, User)
