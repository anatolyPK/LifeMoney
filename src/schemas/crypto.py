from pydantic import BaseModel


class CryptoAsset(BaseModel):
    token: str
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
    token_1: str
    token_2: str
    quantity: float
    is_buy_or_sell: bool
    price_in_usd: float


class TransactionAdd(BaseTransaction):
    pass


class TransactionAddWithUser(BaseTransaction):
    user_id: int


class TransactionRead(BaseTransaction):
    id: int


class TransactionUpdate(BaseTransaction):
    user_id: int


