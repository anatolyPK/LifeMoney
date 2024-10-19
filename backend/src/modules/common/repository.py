from typing import Type, Optional

from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.base.base_model import Base


class AssetSearchManager:
    def __init__(
        self, model: Type[Base], session: AsyncSession, dto_schema: Type[BaseModel]
    ):
        self._model = model
        self._session = session
        self._dto_schema = dto_schema

    async def search_asset(self,
                           asset_name: str,
                           limit: int,
                           offset: int
                           ) -> list[Optional[BaseModel]]:
        async with self._session() as session:
            ilike_expr = or_(
                self._model.symbol.ilike(f"%{asset_name}%"),
                self._model.name.ilike(f"%{asset_name}%"),
            )

            stmt = (
                select(self._model)
                .where(ilike_expr)
                .limit(limit)
                .offset(offset)
            )

            result_orm = await session.scalars(stmt)
            result_dto = [
                self._dto_schema.model_validate(asset) for asset in result_orm
            ]

            return result_dto
