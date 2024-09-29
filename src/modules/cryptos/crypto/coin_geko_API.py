import json

from core.config.project import settings
from utils.aiohttp_manager import AsyncSession


class CoinGekoAPI:
    __api_key = settings.api_keys.API_KEY_CG
    _base_url = "https://api.coingecko.com/api/v3/"
    _headers = {"x-cg-demo-api-key": __api_key, "accept": "application / json"}

    @classmethod
    async def get_token_list(cls) -> list[dict]:
        url = f"{cls._base_url}coins/list"

        parameters = {}
        response_text = await AsyncSession.get(url, cls._headers, parameters)
        data = json.loads(response_text)
        return data

    @classmethod
    async def get_token_price_history(
        cls, coin_id: str, days: int, vs_currency: str = "usd"
    ):
        url = f"{cls._base_url}coins/{coin_id}/market_chart"

        parameters = {
            "vs_currency": vs_currency,
            "days": days,
        }
        response_text = await AsyncSession.get(url, cls._headers, parameters)
        data = json.loads(response_text)
        return data

    @classmethod
    async def get_all_token_info(cls, vs_currency: str = "usd"):
        url = f"{cls._base_url}coins/markets"

        parameters = {
            "vs_currency": vs_currency,
        }
        response_text = await AsyncSession.get(url, cls._headers, parameters)
        data = json.loads(response_text)
        return data


