from base.base_model import ShareTransaction, BondTransaction, EtfTransaction, CurrencyTransaction, FutureTransaction
from modules.common.portfolio import PortfolioMaker, TransactionProcessor
from modules.common.schemas import BaseTransactionSchema, BasePortfolioAsset, BaseAsset
from modules.stocks.schemas import StockPortfolioAsset, StockPortfolioSchema, FutureSchema, CurrencySchema, EtfSchema, \
    BondSchema, ShareSchema
from modules.common.redis_storage import redis_manager



class StockTransactionProcessor(TransactionProcessor):
    def extract_asset(self, transaction: BaseTransactionSchema):
        if transaction.share is not None:
            return transaction.share
        elif transaction.bond is not None:
            return transaction.bond
        elif transaction.etf is not None:
            return transaction.etf
        elif transaction.currency is not None:
            return transaction.currency
        elif transaction.future is not None:
            return transaction.future

    async def add_asset_in_portfolio(self, asset: BaseAsset):
        if asset.id not in self._portfolio_maker._assets:
            current_price = await redis_manager.get_current_price(asset.symbol)

            portfolio_asset = None

            if isinstance(asset, ShareSchema):
                portfolio_asset = self._portfolio_asset_scheme(
                    share=asset,
                    current_price=current_price
                )
            elif isinstance(asset, BondSchema):
                portfolio_asset = self._portfolio_asset_scheme(
                    bond=asset,
                    current_price=current_price
                )
            elif isinstance(asset, EtfSchema):
                portfolio_asset = self._portfolio_asset_scheme(
                    etf=asset,
                    current_price=current_price
                )
            elif isinstance(asset, CurrencySchema):
                portfolio_asset = self._portfolio_asset_scheme(
                    currency=asset,
                    current_price=current_price
                )
            elif isinstance(asset, FutureSchema):
                portfolio_asset = self._portfolio_asset_scheme(
                    future=asset,
                    current_price=current_price
                )

            print('PORTFOLIO ASSET')
            print(portfolio_asset)
            if portfolio_asset is not None:
                self._portfolio_maker._assets[asset.id] = portfolio_asset


class StockPortfolioMaker(PortfolioMaker):
    def __init__(self):
        super().__init__(
            transaction_processor=StockTransactionProcessor,
            portfolio_schema=StockPortfolioSchema,
            portfolio_asset_scheme=StockPortfolioAsset
        )
