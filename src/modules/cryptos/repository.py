from typing import Type

from pydantic import BaseModel
from sqlalchemy import select, case
from sqlalchemy.ext.asyncio import AsyncSession

from base.base_model import Token
from modules.common.repository import AssetSearchManager
from modules.cryptos.schemas import TransactionRead
from src.core.db.database import db_helper
from src.base.base_model import CryptoTransaction
from src.base.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.modules.cryptos.schemas import (
    TransactionAdd,
    TokenSchema,
)


class CryptoRepository(SqlAlchemyRepository[ModelType, TransactionAdd, TransactionAdd]):
    async def get_transactions(
        self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    ) -> list[TransactionRead]:
        results: list[CryptoTransaction] = await super().get_multi(
            order, limit, offset, **filters
        )
        return [TransactionRead.model_validate(transaction) for transaction in results]

    async def get_unique_values(self, column_name: str) -> list:
        async with self._session() as session:
            stmt = (
                select(
                    getattr(self.model, column_name)
                ).distinct()  # Получаем уникальные значения
            )
            row = await session.execute(stmt)
            return row.scalars().all()


class TokenRepository(SqlAlchemyRepository[ModelType, TransactionAdd, TransactionAdd]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession, dto_schema: Type[BaseModel]):
        super().__init__(model, db_session)
        self._asset_searcher = AssetSearchManager(model=model, session=db_session, dto_schema=dto_schema)

    async def insert_multi(self, tokens: list[dict]):
        async with self._session() as session:
            existing_cg_id = await self.check_existing_records('cg_id', [token["id"] for token in tokens])
            orm_data = [
                Token(
                    cg_id=token["id"][:64],
                    name=token["name"][:64],
                    symbol=token["symbol"][:16],
                )
                for token in tokens if token["id"] not in existing_cg_id
            ]
            await super().create_multi(orm_data)

    async def search_token(self, token_symbol: str) -> list[TokenSchema]:
        return await self._asset_searcher.search_asset(token_symbol)


crypro_transactions_repository = CryptoRepository(
    model=CryptoTransaction, db_session=db_helper.get_db_session_context
)

token_repository = TokenRepository(
    model=Token,
    db_session=db_helper.get_db_session_context,
    dto_schema=TokenSchema
)
