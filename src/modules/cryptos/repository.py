from sqlalchemy import select, case

from base.base_model import Token
from src.core.db.database import db_helper
from src.base.base_model import CryptoTransaction
from src.base.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.modules.cryptos.schemas import (
    TransactionAddWithUser,
    TransactionUpdate,
    TokenSchema,
)


class CryptoRepository(
    SqlAlchemyRepository[ModelType, TransactionAddWithUser, TransactionUpdate]
):
    async def get_unique_values(column_name: str) -> list:
        async with self._session() as session:
            stmt = (
                select(getattr(self.model, column_name))
                .distinct()  # Получаем уникальные значения
            )
            row = await session.execute(stmt)
            return row.scalars().all()


class TokenRepository(
    SqlAlchemyRepository[ModelType, TransactionAddWithUser, TransactionUpdate]
):
    async def insert_multi(self, tokens: list[dict]):
        async with self._session() as session:
            token_objects = [
                Token(
                    cg_id=token["id"][:64],
                    name=token["name"][:64],
                    symbol=token["symbol"][:16],
                )
                for token in tokens
            ]
            session.add_all(token_objects)
            await session.commit()

    async def search_token(self, token_symbol: str) -> list[TokenSchema]:
        async with self._session() as session:
            ilike_expr = self.model.symbol.ilike(f"%{token_symbol.strip()}%")
            stmt = select(self.model).where(ilike_expr)

            stmt = (
                stmt.order_by(
                    case(
                        (self.model.symbol == token_symbol.strip(), 0),
                        (
                            self.model.symbol.ilike(
                                f"{token_symbol.strip()}%",
                            ),
                            1,
                        ),
                        else_=2,
                    ),
                    self.model.symbol,
                )
                .limit(100)
                .offset(0)
            )

            result_orm = await session.scalars(stmt)

            result_dto = [
                TokenSchema(id_=token.id, name=token.name, symbol=token.symbol, cg_id=token.cg_id)
                for token in result_orm
            ]

            return result_dto


crypro_transactions_repository = CryptoRepository(
    model=CryptoTransaction, db_session=db_helper.get_db_session_context
)

token_repository = TokenRepository(
    model=Token, db_session=db_helper.get_db_session_context
)
