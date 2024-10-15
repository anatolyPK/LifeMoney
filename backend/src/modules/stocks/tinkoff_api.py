import json
from typing import Optional

from backend.src.core.config.project import settings
from backend.src.utils.aiohttp_manager import AsyncSession


class TinkoffAPI:
    __api_key = settings.api_keys.API_KEY_TINKOFF
    _base_url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1."
    _parameters = {}
    _headers = {
        "Authorization": f"Bearer {__api_key}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    _data = {
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED",
    }

    @classmethod
    async def get_candles(cls, figi: str, from_: str, to: str, interval: str):
        url = f"{cls._base_url}MarketDataService/GetCandles"
        data = {
            'figi': figi,
            "from": "2023-10-01T12:54:01.402Z",
            "to": "2024-10-01T12:54:01.402Z",
            "interval": "5"
        }

        response_text = await AsyncSession.post(
            url=url,
            headers=cls._headers,
            params=cls._parameters,
            data=data
        )
        data = json.loads(response_text)
        return data

    @classmethod
    async def get_current_prices(cls, figis: list[str]) -> dict[list[Optional[dict]]]:
        url = f"{cls._base_url}MarketDataService/GetLastPrices"
        response_text = await AsyncSession.post(
            url=url,
            headers=cls._headers,
            params=cls._parameters,
            data={
                "instrument_id": figis,
                'last_price_type': 'LAST_PRICE_EXCHANGE'
            }
        )
        data = json.loads(response_text)
        return data

    @classmethod
    async def get_shares(cls) -> list[dict]:
        return await cls._get_assets("Shares")

    @classmethod
    async def get_bonds(cls) -> list[dict]:
        return await cls._get_assets("Bonds")

    @classmethod
    async def get_currencies(cls) -> list[dict]:
        return await cls._get_assets("Currencies")

    @classmethod
    async def get_etfs(cls) -> list[dict]:
        return await cls._get_assets("Etfs")

    @classmethod
    async def get_futures(cls) -> list[dict]:
        return await cls._get_assets("Futures")

    @classmethod
    async def _get_assets(cls, assets_name: str):
        url = f"{cls._base_url}InstrumentsService/{assets_name}"
        response_text = await AsyncSession.post(
            url, cls._headers, cls._parameters, cls._data
        )
        data = json.loads(response_text)
        return data
