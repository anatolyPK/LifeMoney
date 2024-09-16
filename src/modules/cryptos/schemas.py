from typing import Optional

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


class MainPortfolioInfo(BaseModel):
    total_value: float
    total_investment: float
    total_profit_in_currency: float
    total_profit_in_percent: float


class CryptoPortfolio(BaseModel):
    main_info: MainPortfolioInfo
    assets: list[CryptoAsset]


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation: OperationEnum
    quantity: float
    price_in_usd: float

    timestamp: int


class TransactionAdd(BaseTransaction):
    token_id: int
    user_id: Optional[int] = None


class TransactionRead(BaseTransaction):
    token: TokenSchema
    id: int
