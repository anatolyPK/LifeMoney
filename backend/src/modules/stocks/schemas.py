import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.src.modules.common.schemas import (
    BaseTransactionSchema,
    BaseAsset,
    BasePortfolioSchema,
    BasePortfolioAsset,
)


class BaseStockAssetSchema(BaseAsset):
    figi: str
    currency: str
    buy_available_flag: bool
    sell_available_flag: bool
    for_iis_flag: bool
    for_qual_investor_flag: bool
    exchange: str


class ShareSchema(BaseStockAssetSchema):
    lot: int
    nominal: float
    country_of_risk: str
    sector: str
    div_yield_flag: bool


class BondSchema(BaseStockAssetSchema):
    nominal: float
    initial_nominal: float
    aci_value: float
    country_of_risk: str
    sector: str
    floating_coupon_flag: bool
    perpetual_flag: bool
    amortization_flag: bool


class EtfSchema(BaseStockAssetSchema):
    fixed_commission: float
    focus_type: str
    country_of_risk: str
    sector: str


class CurrencySchema(BaseStockAssetSchema):
    lot: int
    nominal: float
    country_of_risk: str
    min_price_increment: float


class FutureSchema(BaseStockAssetSchema):
    lot: int
    short_enabled_flag: bool
    last_trade_day: datetime
    futures_type: str
    asset_type: str
    country_of_risk: str
    sector: str
    expiration_date: datetime
    min_price_increment_amount: float


class AssetsSearchResultsSchema(BaseModel):
    shares: Optional[list[ShareSchema]] = []
    bonds: Optional[list[BondSchema]] = []
    etfs: Optional[list[EtfSchema]] = []
    currencies: Optional[list[CurrencySchema]] = []
    futures: Optional[list[FutureSchema]] = []


class AddTransactionSchema(BaseTransactionSchema):
    user_id: Optional[uuid.UUID] = None

    share_id: Optional[int] = None
    bond_id: Optional[int] = None
    etf_id: Optional[int] = None
    currency_id: Optional[int] = None
    future_id: Optional[int] = None


class AddShareSchema(BaseTransactionSchema):
    user_id: uuid.UUID
    share_id: int


class AddBondSchema(BaseTransactionSchema):
    user_id: uuid.UUID
    bond_id: int


class AddEtfSchema(BaseTransactionSchema):
    user_id: uuid.UUID
    etf_id: int


class AddCurrencySchema(BaseTransactionSchema):
    user_id: uuid.UUID
    currency_id: int


class AddFutureSchema(BaseTransactionSchema):
    user_id: uuid.UUID
    future_id: int


class ReadTransactionSchema(BaseTransactionSchema):
    id: int

    share: Optional[ShareSchema] = None
    bond: Optional[BondSchema] = None
    etf: Optional[EtfSchema] = None
    currency: Optional[CurrencySchema] = None
    future: Optional[FutureSchema] = None


class StockPortfolioAssetSchema(BasePortfolioAsset):
    share: Optional[ShareSchema] = None
    bond: Optional[BondSchema] = None
    etf: Optional[EtfSchema] = None
    currency: Optional[CurrencySchema] = None
    future: Optional[FutureSchema] = None


class StockPortfolioSchema(BasePortfolioSchema):
    assets: list[StockPortfolioAssetSchema]
