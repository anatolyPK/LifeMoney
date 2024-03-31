import datetime

from pydantic import BaseModel

from src.models.auth import User


class BaseTransaction(BaseModel):
    pass


class TransactionAdd(BaseTransaction):
    token_1: str
    token_2: str
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float


class TransactionAddWithUser(BaseTransaction):
    token_1: str
    token_2: str
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float
    user_id: int


class TransactionRead(BaseTransaction):
    id: int
    token_1: str
    token_2: str
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float


class TransactionUpdate(BaseTransaction):
    token_1: str
    token_2: str
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float
    user_id: int

