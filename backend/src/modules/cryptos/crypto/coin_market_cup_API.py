import json

from backend.src.core.config.project import settings
from backend.src.utils.aiohttp_manager import AsyncSession
from backend.src.utils.schemas import CryptocurrencyListingsValidate


class CoinMarketCupAPI:
    __api_key = settings.api_keys.API_KEY_CMC

    @classmethod
    async def get_cryptocurrency_listings(cls, limit: int = 100):
        query = CryptocurrencyListingsValidate(limit=limit)
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": cls.__api_key,
        }
        parameters = {
            "limit": query.limit,
        }
        response_text = await AsyncSession.get(url, headers, parameters)
        data = json.loads(response_text)
        return data
