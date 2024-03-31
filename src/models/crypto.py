# from sqlalchemy import ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models import Base
#
#
# from typing import TYPE_CHECKING
#
#
# if TYPE_CHECKING:
#     from src.auth.models import User
#
#
# class CryptoTransaction(Base):
#     __tablename__ = 'crypto_transaction'
#
#     user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))
#     token_1: Mapped[str] = mapped_column(String(16))
#     token_2: Mapped[str] = mapped_column(String(16))
#     quantity: Mapped[float]
#     is_buy_or_sell: Mapped[bool] = mapped_column(default=True)
#     price_in_usd: Mapped[float] = mapped_column(default=0)
#
#     user: Mapped['User'] = relationship(back_populates='crypto_transactions')
