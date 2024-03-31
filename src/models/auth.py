from typing import Any, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

from src.models.base_model import Base

if TYPE_CHECKING:
    from src.models.crypto import CryptoTransaction


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    
    username: Mapped[str] = mapped_column(String(16), unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id', ondelete='CASCADE'))

    role: Mapped['Role'] = relationship(back_populates='users')
    crypto_transactions: Mapped[List['CryptoTransaction']] = relationship(back_populates='user')


class Role(Base):
    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(String(16), unique=True)
    permission: Mapped[dict[str, Any]] = mapped_column(nullable=True)

    users: Mapped[list['User']] = relationship(back_populates='role')


class CryptoTransaction(Base):
    """Вспомогательная таблица для CryptoTransaction
        Не получается создавать таблицу в другом модуле..."""
    __tablename__ = 'crypto_transaction'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    token_1: Mapped[str] = mapped_column(String(16))
    token_2: Mapped[str] = mapped_column(String(16))
    quantity: Mapped[float]
    is_buy_or_sell: Mapped[bool] = mapped_column(default=True)
    price_in_usd: Mapped[float] = mapped_column(default=0)

    user: Mapped['User'] = relationship(back_populates='crypto_transactions')
