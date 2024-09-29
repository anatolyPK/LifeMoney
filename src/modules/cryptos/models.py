# from sqlalchemy import ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.base.base_model import Base
#
#
# class CryptoTransaction(Base):
#     __tablename__ = 'crypto_transaction'
#
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
#     token_1: Mapped[str] = mapped_column(String(16))
#     token_2: Mapped[str] = mapped_column(String(16))
#     quantity: Mapped[float]
#     is_buy_or_sell: Mapped[bool] = mapped_column(default=True)
#     price: Mapped[float] = mapped_column(default=0)
#
#     user: Mapped['src.auth.models.User'] = relationship(back_populates='crypto_transactions')
