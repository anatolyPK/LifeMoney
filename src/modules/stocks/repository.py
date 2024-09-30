import asyncio
from typing import Type, Optional, Generic, Any
from itertools import chain
from operator import attrgetter

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base.base_model import Share, Future, Currency, Etf, Bond, ShareTransaction, BondTransaction, EtfTransaction, \
    CurrencyTransaction, FutureTransaction, CommonAssetsInfo
from modules.common.repository import AssetSearchManager
from modules.stocks.schemas import ShareSchema, BondSchema, EtfSchema, CurrencySchema, FutureSchema, \
    AddTransactionSchema, AddShareSchema, AddBondSchema, AddEtfSchema, AddCurrencySchema, \
    AddFutureSchema, ReadTransactionSchema
from src.core.db.database import db_helper
from src.base.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.modules.cryptos.schemas import (
    TransactionAdd,
)
from src.modules.stocks.exceptions import MissingTransactionIdError
from src.modules.stocks.utils import (
    convert_tinkoff_money_in_currency,
    convert_str_to_datetime,
)


class StockTransactionsRepository(
    SqlAlchemyRepository[ModelType, TransactionAdd, TransactionAdd]
):
    async def update(self, transaction: AddTransactionSchema, id=id):
        transaction_data = transaction.model_dump(exclude_none=True)

        transaction_map = {
            'share_id': (AddShareSchema, share_transaction_repository),
            'bond_id': (AddBondSchema, bond_transaction_repository),
            'etf_id': (AddEtfSchema, etf_transaction_repository),
            'currency_id': (AddCurrencySchema, currency_transaction_repository),
            'future_id': (AddFutureSchema, future_transaction_repository),
        }

        for id_key, (schema, repository) in transaction_map.items():
            if getattr(transaction, id_key) > 0:
                transaction_instance = schema(
                    **transaction_data,
                    asset_id=transaction_data.get(id_key)
                )
                await repository.update(transaction_instance, id=id)
                return await repository.get_single(id=id)

        raise MissingTransactionIdError

    async def create_transaction(self, transaction: AddTransactionSchema):
        transaction_data = transaction.model_dump(exclude_none=True)

        transaction_map = {
            'share_id': (AddShareSchema, share_transaction_repository),
            'bond_id': (AddBondSchema, bond_transaction_repository),
            'etf_id': (AddEtfSchema, etf_transaction_repository),
            'currency_id': (AddCurrencySchema, currency_transaction_repository),
            'future_id': (AddFutureSchema, future_transaction_repository),
        }

        for id_key, (schema, repository) in transaction_map.items():
            if getattr(transaction, id_key) > 0:
                transaction_instance = schema(
                    **transaction_data,
                    asset_id=transaction_data.get(id_key)
                )
                return await repository.create(transaction_instance)

        raise MissingTransactionIdError

    async def get_user_transaction(
            self,
            order: str = "timestamp",
            limit: int = 100,
            offset: int = 0,
            **filters
    ) -> list[ReadTransactionSchema]:
        tasks = [
            repository.get_transactions(order, limit, offset, **filters)
            for repository in (share_transaction_repository, bond_transaction_repository, etf_transaction_repository,
                               currency_transaction_repository, future_transaction_repository)
        ]
        results = await asyncio.gather(*tasks)

        flat_list = list(chain.from_iterable(results))
        sorted_list = sorted(flat_list, key=attrgetter('timestamp'), reverse=True)
        return sorted_list


class BaseTransactionRepository(SqlAlchemyRepository[ModelType, TransactionAdd, TransactionAdd], Generic[ModelType]):
    async def get_transactions(
            self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    ) -> list[ReadTransactionSchema]:
        results: list[ModelType] = await super().get_multi(order, limit, offset, **filters)
        print(results)
        return [ReadTransactionSchema.model_validate(transaction) for transaction in results]

    async def get_unique_figis(
            self,
            asset_model: CommonAssetsInfo,
            asset_filed: str,
            limit: int = 100,
            offset: int = 0
    ) -> list[str]:
        async with self._session() as session:
            _assets_filed = getattr(self.model, asset_filed)
            stmt = (
                select(self.model)
                .join(asset_model)
                .filter(_assets_filed == asset_model.id)
                .distinct()
                .limit(limit)
                .offset(offset)
            )
            row = await session.execute(stmt)
            results = row.scalars().all()
            return [getattr(result, asset_filed[:-3]).figi for result in results]

class ShareTransactionRepository(BaseTransactionRepository[ShareTransaction]):
    async def get_unique_figis(self, limit: int = 100, offset: int = 0) -> list[str]:
        return await super().get_unique_figis(Share, 'share_id', limit, offset)

    # async def get_transactions(
    #         self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    # ) -> dict[str, list[ReadTransactionSchema]]:
    #     results = await super().get_transactions(order, limit, offset, **filters)
    #     return {'shares': results}

class BondTransactionRepository(BaseTransactionRepository[BondTransaction]):
    async def get_unique_figis(self, limit: int = 100, offset: int = 0) -> list[str]:
        return await super().get_unique_figis(Bond, 'bond_id', limit, offset)

    # async def get_transactions(
    #         self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    # ) -> dict[str, list[ReadTransactionSchema]]:
    #     results = await super().get_transactions(order, limit, offset, **filters)
    #     return {'bonds': results}

class EtfTransactionRepository(BaseTransactionRepository[EtfTransaction]):
    async def get_unique_figis(self, limit: int = 100, offset: int = 0) -> list[str]:
        return await super().get_unique_figis(Etf, 'etf_id', limit, offset)
    #
    # async def get_transactions(
    #         self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    # ) -> dict[str, list[ReadTransactionSchema]]:
    #     results = await super().get_transactions(order, limit, offset, **filters)
    #     return {'etfs': results}

class CurrencyTransactionRepository(BaseTransactionRepository[CurrencyTransaction]):
    async def get_unique_figis(self, limit: int = 100, offset: int = 0) -> list[str]:
        return await super().get_unique_figis(Currency, 'currency_id', limit, offset)

    # async def get_transactions(
    #         self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    # ) -> dict[str, list[ReadTransactionSchema]]:
    #     results = await super().get_transactions(order, limit, offset, **filters)
    #     return {'currencies': results}

class FutureTransactionRepository(BaseTransactionRepository[FutureTransaction]):
    async def get_unique_figis(self, limit: int = 100, offset: int = 0) -> list[str]:
        return await super().get_unique_figis(Future, 'future_id', limit, offset)

    # async def get_transactions(
    #         self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    # ) -> dict[str, list[ReadTransactionSchema]]:
    #     results = await super().get_transactions(order, limit, offset, **filters)
    #     return {'futures': results}

class BaseAssetRepository(SqlAlchemyRepository[ModelType, TransactionAdd, TransactionAdd]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession, dto_schema: Type[BaseModel]):
        super().__init__(model, db_session)
        self._asset_search = AssetSearchManager(model=model, session=db_session, dto_schema=dto_schema)

    async def search_asset(self, asset_name: str) -> list[Optional[ShareSchema]]:
        return await self._asset_search.search_asset(asset_name)

    async def create_multi(
            self,
            data: list[dict[str, Any]]
    ):
        existing_figis = await self.check_existing_records('figi', [data_dict["figi"] for data_dict in data])
        orm_data = [self.create_asset(data_dict) for data_dict in data if data_dict["figi"] not in existing_figis]
        await super().create_multi(orm_data)

    def create_asset(self, data_dict: dict[str, Any]):
        raise NotImplemented


class ShareRepository(BaseAssetRepository[Share]):
    def create_asset(self, data_dict: dict[str, Any]) -> Share:
        return Share(
            figi=data_dict["figi"],
            symbol=data_dict["ticker"],
            name=data_dict["name"],
            currency=data_dict["currency"],
            buy_available_flag=data_dict["buyAvailableFlag"],
            sell_available_flag=data_dict["sellAvailableFlag"],
            for_iis_flag=data_dict["forIisFlag"],
            for_qual_investor_flag=data_dict["forQualInvestorFlag"],
            exchange=data_dict["exchange"],
            lot=data_dict["lot"],
            nominal=convert_tinkoff_money_in_currency(data_dict["nominal"]),
            country_of_risk=data_dict["countryOfRisk"],
            sector=data_dict["sector"],
            div_yield_flag=data_dict["divYieldFlag"],
        )


class BondRepository(BaseAssetRepository[Bond]):
    def create_asset(self, data_dict: dict[str, Any]) -> Bond:
        return Bond(
            figi=data_dict["figi"],
            symbol=data_dict["ticker"],
            name=data_dict["name"],
            currency=data_dict["currency"],
            buy_available_flag=data_dict["buyAvailableFlag"],
            sell_available_flag=data_dict["sellAvailableFlag"],
            for_iis_flag=data_dict["forIisFlag"],
            for_qual_investor_flag=data_dict["forQualInvestorFlag"],
            exchange=data_dict["exchange"],
            nominal=convert_tinkoff_money_in_currency(data_dict["nominal"]),
            initial_nominal=convert_tinkoff_money_in_currency(data_dict["initialNominal"]),
            aci_value=convert_tinkoff_money_in_currency(data_dict["aciValue"]),
            country_of_risk=data_dict["countryOfRisk"],
            sector=data_dict["sector"],
            floating_coupon_flag=data_dict["floatingCouponFlag"],
            perpetual_flag=data_dict["perpetualFlag"],
            amortization_flag=data_dict["amortizationFlag"],
        )


class EtfRepository(BaseAssetRepository[Etf]):
    def create_asset(self, data_dict: dict[str, Any]) -> Etf:
        return Etf(
            figi=data_dict["figi"],
            symbol=data_dict["ticker"],
            name=data_dict["name"],
            currency=data_dict["currency"],
            buy_available_flag=data_dict["buyAvailableFlag"],
            sell_available_flag=data_dict["sellAvailableFlag"],
            for_iis_flag=data_dict["forIisFlag"],
            for_qual_investor_flag=data_dict["forQualInvestorFlag"],
            exchange=data_dict["exchange"],
            fixed_commission=convert_tinkoff_money_in_currency(
                data_dict.get("fixedCommission", {'units': 0, 'nano': 0})
            ),
            focus_type=data_dict["focusType"],
            country_of_risk=data_dict["countryOfRisk"],
            sector=data_dict["sector"],
        )

class CurrencyRepository(BaseAssetRepository[Currency]):
    def create_asset(self, data_dict: dict[str, Any]) -> Currency:
        return Currency(
            figi=data_dict["figi"],
            symbol=data_dict["ticker"],
            name=data_dict["name"],
            currency=data_dict["currency"],
            buy_available_flag=data_dict["buyAvailableFlag"],
            sell_available_flag=data_dict["sellAvailableFlag"],
            for_iis_flag=data_dict["forIisFlag"],
            for_qual_investor_flag=data_dict["forQualInvestorFlag"],
            exchange=data_dict["exchange"],
            lot=data_dict["lot"],
            nominal=convert_tinkoff_money_in_currency(data_dict["nominal"]),
            country_of_risk=data_dict["countryOfRisk"],
            min_price_increment=convert_tinkoff_money_in_currency(data_dict["minPriceIncrement"])
        )

class FutureRepository(BaseAssetRepository[Future]):
    def create_asset(self, data_dict: dict[str, Any]) -> Future:
        return Future(
            figi=data_dict["figi"],
            symbol=data_dict["ticker"],
            name=data_dict["name"],
            currency=data_dict["currency"],
            buy_available_flag=data_dict["buyAvailableFlag"],
            sell_available_flag=data_dict["sellAvailableFlag"],
            for_iis_flag=data_dict["forIisFlag"],
            for_qual_investor_flag=data_dict["forQualInvestorFlag"],
            exchange=data_dict["exchange"],
            lot=data_dict["lot"],
            short_enabled_flag=data_dict["shortEnabledFlag"],
            last_trade_day=convert_str_to_datetime(data_dict["lastTradeDate"]),
            futures_type=data_dict["futuresType"],
            asset_type=data_dict["assetType"],
            country_of_risk=data_dict["countryOfRisk"],
            sector=data_dict["sector"],
            expiration_date=convert_str_to_datetime(data_dict["expirationDate"]),
            min_price_increment_amount=convert_tinkoff_money_in_currency(min_price)
            if (min_price := data_dict.get("minPriceIncrementAmount"))
            else 0,
        )


share_repository = ShareRepository(
    model=Share,
    db_session=db_helper.get_db_session_context,
    dto_schema=ShareSchema
)

bond_repository = BondRepository(
    model=Bond,
    db_session=db_helper.get_db_session_context,
    dto_schema=BondSchema
)

etf_repository = EtfRepository(
    model=Etf,
    db_session=db_helper.get_db_session_context,
    dto_schema=EtfSchema
)

currency_repository = CurrencyRepository(
    model=Currency,
    db_session=db_helper.get_db_session_context,
    dto_schema=CurrencySchema
)

future_repository = FutureRepository(
    model=Future,
    db_session=db_helper.get_db_session_context,
    dto_schema=FutureSchema
)

stock_repository = StockTransactionsRepository(  # что это
    model=Future, db_session=db_helper.get_db_session_context
)

share_transaction_repository = ShareTransactionRepository(
    model=ShareTransaction, db_session=db_helper.get_db_session_context
)

bond_transaction_repository = BondTransactionRepository(
    model=BondTransaction, db_session=db_helper.get_db_session_context
)

currency_transaction_repository = CurrencyTransactionRepository(
    model=CurrencyTransaction, db_session=db_helper.get_db_session_context
)

etf_transaction_repository = EtfTransactionRepository(
    model=EtfTransaction, db_session=db_helper.get_db_session_context
)

future_transaction_repository = FutureTransactionRepository(
    model=FutureTransaction, db_session=db_helper.get_db_session_context
)
