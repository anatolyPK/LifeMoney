from src.config.db.database import db_helper
from src.models.auth import CryptoTransaction
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.schemas.crypto import TransactionAddWithUser, TransactionUpdate


class CryptoRepository(SqlAlchemyRepository[ModelType, TransactionAddWithUser, TransactionUpdate]):
    pass


crypro_repository = CryptoRepository(model=CryptoTransaction,
                                     db_session=db_helper.get_db_session_context)
