import enum
from datetime import datetime
from typing import Any

from sqlalchemy.types import JSON
from sqlalchemy import TIMESTAMP, func, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

import uuid
from typing import List

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, Boolean, Uuid
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    type_annotation_map = {dict[str, Any]: JSON}

    repr_cols_num = 3
    repr_cols = []

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f'<{self.__class__.__name__} {", ".join(cols)}'

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(String(16), unique=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"))

    role: Mapped["Role"] = relationship(back_populates="users")
    crypto_transactions: Mapped[List["CryptoTransaction"]] = relationship(
        back_populates="user"
    )
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="rt_user"
    )
    share_transactions: Mapped[list["ShareTransaction"]] = relationship(
        back_populates="user"
    )
    bond_transactions: Mapped[list["BondTransaction"]] = relationship(
        back_populates="user"
    )
    etf_transactions: Mapped[list["EtfTransaction"]] = relationship(
        back_populates="user"
    )
    currency_transactions: Mapped[list["CurrencyTransaction"]] = relationship(
        back_populates="user"
    )
    future_transactions: Mapped[list["FutureTransaction"]] = relationship(
        back_populates="user"
    )


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}  # < new

    name: Mapped[str] = mapped_column(String(16), unique=True)
    permission: Mapped[dict[str, Any]] = mapped_column(nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    refresh_token: Mapped[str] = mapped_column(unique=True)
    fingerprint: Mapped[str] = mapped_column(String(250))
    should_deleted_at: Mapped[datetime]

    rt_user: Mapped["User"] = relationship(back_populates="refresh_tokens")


class OperationEnum(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class CryptoTransaction(Base):
    __tablename__ = "crypto_transaction"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    token_id: Mapped[int] = mapped_column(ForeignKey("token.id", ondelete="CASCADE"))
    quantity: Mapped[float]
    operation: Mapped[OperationEnum] = mapped_column(Enum(OperationEnum))
    price: Mapped[float]
    timestamp: Mapped[int]

    token: Mapped["Token"] = relationship(
        "Token",
        foreign_keys=[token_id],
        back_populates="token_transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="crypto_transactions")


class Token(Base):
    __tablename__ = "token"

    cg_id: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    symbol: Mapped[str] = mapped_column(String(16))

    token_transactions: Mapped[list["CryptoTransaction"]] = relationship(
        "CryptoTransaction",
        back_populates="token",
        foreign_keys=[CryptoTransaction.token_id],
    )


class CommonAssetsInfo(Base):
    __abstract__ = True

    figi: Mapped[str]
    symbol: Mapped[str]
    name: Mapped[str]
    currency: Mapped[str]
    buy_available_flag: Mapped[bool]
    sell_available_flag: Mapped[bool]
    for_iis_flag: Mapped[bool]
    for_qual_investor_flag: Mapped[bool]
    exchange: Mapped[str]


class Share(CommonAssetsInfo):
    __tablename__ = "share"

    lot: Mapped[int]
    nominal: Mapped[float]
    country_of_risk: Mapped[str]
    sector: Mapped[str]
    div_yield_flag: Mapped[bool]

    transactions: Mapped[list["ShareTransaction"]] = relationship(
        back_populates="share"
    )


class Bond(CommonAssetsInfo):
    __tablename__ = "bond"

    nominal: Mapped[float]
    initial_nominal: Mapped[float]
    aci_value: Mapped[float]
    country_of_risk: Mapped[str]
    sector: Mapped[str]
    floating_coupon_flag: Mapped[bool]
    perpetual_flag: Mapped[bool]
    amortization_flag: Mapped[bool]

    transactions: Mapped[list["BondTransaction"]] = relationship(back_populates="bond")


class Etf(CommonAssetsInfo):
    __tablename__ = "etf"

    fixed_commission: Mapped[float]
    focus_type: Mapped[str]
    country_of_risk: Mapped[str]
    sector: Mapped[str]

    transactions: Mapped[list["EtfTransaction"]] = relationship(back_populates="etf")


class Currency(CommonAssetsInfo):
    __tablename__ = "currency"

    lot: Mapped[int]
    nominal: Mapped[float]
    country_of_risk: Mapped[str]
    min_price_increment: Mapped[float]
    transactions: Mapped[list["CurrencyTransaction"]] = relationship(
        back_populates="currency"
    )


class Future(CommonAssetsInfo):
    __tablename__ = "future"

    lot: Mapped[int]
    short_enabled_flag: Mapped[bool]
    last_trade_day: Mapped[datetime]
    futures_type: Mapped[str]
    asset_type: Mapped[str]
    country_of_risk: Mapped[str]
    sector: Mapped[str]
    expiration_date: Mapped[datetime]
    min_price_increment_amount: Mapped[float]

    transactions: Mapped[list["FutureTransaction"]] = relationship(
        back_populates="future"
    )


class CommonAssetsTransaction(Base):
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    quantity: Mapped[float]
    operation: Mapped[OperationEnum] = mapped_column(Enum(OperationEnum))
    price: Mapped[float]
    timestamp: Mapped[int]


class ShareTransaction(CommonAssetsTransaction):
    __tablename__ = "share_transaction"

    share_id: Mapped[int] = mapped_column(ForeignKey("share.id", ondelete="CASCADE"))

    share: Mapped["Share"] = relationship(
        "Share",
        foreign_keys=[share_id],
        back_populates="transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="share_transactions")


class BondTransaction(CommonAssetsTransaction):
    __tablename__ = "bond_transaction"

    bond_id: Mapped[int] = mapped_column(ForeignKey("bond.id", ondelete="CASCADE"))

    bond: Mapped["Bond"] = relationship(
        "Bond",
        foreign_keys=[bond_id],
        back_populates="transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="bond_transactions")


class EtfTransaction(CommonAssetsTransaction):
    __tablename__ = "etf_transaction"

    etf_id: Mapped[int] = mapped_column(ForeignKey("etf.id", ondelete="CASCADE"))

    etf: Mapped[Etf] = relationship(
        "Etf",
        foreign_keys=[etf_id],
        back_populates="transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="etf_transactions")


class CurrencyTransaction(CommonAssetsTransaction):
    __tablename__ = "currency_transaction"

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currency.id", ondelete="CASCADE")
    )

    currency: Mapped[Currency] = relationship(
        "Currency",
        foreign_keys=[currency_id],
        back_populates="transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="currency_transactions")


class FutureTransaction(CommonAssetsTransaction):
    __tablename__ = "future_transaction"

    future_id: Mapped[int] = mapped_column(ForeignKey("future.id", ondelete="CASCADE"))

    future: Mapped[Future] = relationship(
        "Future",
        foreign_keys=[future_id],
        back_populates="transactions",
        lazy="joined",
    )

    user: Mapped["User"] = relationship(back_populates="future_transactions")
