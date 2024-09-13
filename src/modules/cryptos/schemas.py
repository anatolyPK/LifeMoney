import uuid

from pydantic import BaseModel, ConfigDict

from base.base_model import OperationEnum


class TokenSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    symbol: str
    cg_id: str


class CryptoAsset(BaseModel):
    token: TokenSchema
    quantity: float = 0
    average_price_buy: float = 0

    balance: float = 0
    current_price: float = 0
    profit_in_currency: float = 0
    profit_in_percent: float = 0
    percent_of_portfolio: float = 0


class CryptoPortfolio(BaseModel):
    total: float
    assets: list[CryptoAsset]


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token_1: TokenSchema
    token_2: TokenSchema
    quantity: float
    operation: OperationEnum
    price_in_usd: float
    timestamp: int


class TransactionAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token_1_id: int
    token_2_id: int
    quantity: float
    operation: OperationEnum
    price_in_usd: float
    timestamp: int


class TransactionAddWithUser(TransactionAdd):
    user_id: uuid.UUID


class TransactionRead(BaseTransaction):
    id: int


class TransactionUpdate(BaseTransaction):
    user_id: uuid.UUID
