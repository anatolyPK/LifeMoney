from src.core.db.database import db_helper
from src.base.base_model import CryptoTransaction
from src.base.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.modules.cryptos.schemas import TransactionAddWithUser, TransactionUpdate


class CryptoRepository(SqlAlchemyRepository[ModelType, TransactionAddWithUser, TransactionUpdate]):
    pass


crypro_repository = CryptoRepository(model=CryptoTransaction,
                                     db_session=db_helper.get_db_session_context)
