# import uuid
# from datetime import datetime
# from typing import Any, List, TYPE_CHECKING
#
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy import TIMESTAMP, func, String, ForeignKey, Boolean, Uuid
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# # from src.modules.cryptos.models import CryptoTransaction
# from src.base.base_model import Base
#
#
# class User(Base):
#     __tablename__ = "user"
#     __table_args__ = {"extend_existing": True}
#
#     id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
#
#     username: Mapped[str] = mapped_column(String(16), unique=True)
#     email: Mapped[str] = mapped_column(
#         String(length=320), unique=True, index=True, nullable=False
#     )
#     hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
#
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
#     role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"))
#
#     role: Mapped["src.auth.models.Role"] = relationship(back_populates="users")
#     # crypto_transactions: Mapped[List["CryptoTransaction"]] = relationship(back_populates="user")
#     refresh_tokens: Mapped[List["src.auth.models.RefreshToken"]] = relationship(back_populates="rt_user")
#
# class Role(Base):
#     __tablename__ = 'role'
#     __table_args__ = {"extend_existing": True}  # < new
#
#     name: Mapped[str] = mapped_column(String(16), unique=True)
#     permission: Mapped[dict[str, Any]] = mapped_column(nullable=True)
#
#     users: Mapped[list['src.auth.models.User']] = relationship(back_populates='role')
#
#
# class RefreshToken(Base):
#     __tablename__ = "refresh_token"
#     __table_args__ = {'extend_existing': True}
#
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
#     refresh_token: Mapped[str] = mapped_column(unique=True)
#     fingerprint: Mapped[str] = mapped_column(String(250))
#     should_deleted_at: Mapped[datetime]
#
#     rt_user: Mapped["src.auth.models.User"] = relationship(back_populates="refresh_tokens")
