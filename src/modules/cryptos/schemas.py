import uuid

from pydantic import BaseModel


class TokenSchema(BaseModel):
    id_: int
    name: str
    symbol: str
    cg_id: str
# Token cg_id=aadex-finance, name=AADex Finance, symbol=ade

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
    token_1_id: int
    token_2_id: int
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float
    timestamp: int


class TransactionAdd(BaseTransaction):
    pass


class TransactionAddWithUser(BaseTransaction):
    user_id: uuid.UUID


class TransactionRead(BaseTransaction):
    id: int


class TransactionUpdate(BaseTransaction):
    user_id: uuid.UUID
