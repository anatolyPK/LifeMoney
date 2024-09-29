from typing import Type, TypeVar, Optional, Generic

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.base_repository import AbstractRepository
from src.base.base_model import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqlAlchemyRepository(
    AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self._session = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session() as session:
            instance = self.model(**data.model_dump())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def create_multi(self, data: list[CreateSchemaType]):
        async with self._session() as session:
            session.add_all(data)
            await session.commit()

    async def check_existing_records(self, unique_field: str, values: list) -> set:
        async with self._session() as session:
            result = await session.execute(
                select(self.model).where(getattr(self.model, unique_field).in_(values))
            )
            existing_records = result.scalars().all()
            return {getattr(record, unique_field) for record in existing_records}

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self._session() as session:
            stmt = (
                update(self.model)
                .values(**data.dict())
                .filter_by(**filters)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        async with self._session() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            return row.scalar_one_or_none()

    async def get_multi(
        self, order: str = "id", limit: int = 100, offset: int = 0, **filters
    ) -> list[ModelType]:
        async with self._session() as session:
            stmt = (
                select(self.model)
                .filter_by(**filters)
                .order_by(order)
                .limit(limit)
                .offset(offset)
            )
            row = await session.execute(stmt)
            return row.scalars().all()
