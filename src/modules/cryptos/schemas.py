from typing import Optional

from modules.common.schemas import BaseTransactionSchema, BasePortfolioAsset, BaseAsset, BasePortfolioSchema


class TokenSchema(BaseAsset):
    cg_id: str


class CryptoPortfolioAsset(BasePortfolioAsset):
    asset: TokenSchema


class TransactionAdd(BaseTransactionSchema):
    token_id: int
    user_id: Optional[int] = None


class TransactionRead(BaseTransactionSchema):
    token: TokenSchema
    id: int


class CryptoPortfolioSchema(BasePortfolioSchema):
    assets: list[CryptoPortfolioAsset]