import enum

from pydantic import BaseModel, ConfigDict

from base.base_model import OperationEnum


class CurrencyEnum(str, enum.Enum):
    usd: str = "usd"
    rub: str = "rub"


class BaseAsset(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    symbol: str  # or ticker


class BasePortfolioAsset(BaseModel):
    quantity: float = 0
    average_price_buy: float = 0
    currency_: CurrencyEnum = CurrencyEnum.usd

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


class BaseTransactionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation: OperationEnum
    quantity: float
    price: float = None

    timestamp: int


class BasePortfolioSchema(BaseModel):
    main_info: MainPortfolioInfo
