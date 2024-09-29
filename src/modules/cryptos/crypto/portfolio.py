from modules.common.portfolio import PortfolioMaker, TransactionProcessor
from modules.common.schemas import BaseTransactionSchema, BasePortfolioAsset
from modules.cryptos.schemas import CryptoPortfolioAsset, CryptoPortfolioSchema
from modules.stocks.schemas import StockPortfolioAsset


class CryptoTransactionProcessor(TransactionProcessor):

    def extract_asset(self, transaction: BaseTransactionSchema):
        return transaction.token


class CryptoPortfolioMaker(PortfolioMaker):
    def __init__(self):
        super().__init__(
            transaction_processor=CryptoTransactionProcessor,
            portfolio_schema=CryptoPortfolioSchema,
            portfolio_asset_scheme=CryptoPortfolioAsset
        )
