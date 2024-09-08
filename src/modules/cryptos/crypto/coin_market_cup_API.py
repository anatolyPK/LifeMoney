import asyncio
import os
import json
from dotenv import load_dotenv

from src.utils.aiohttp_manager import AsyncSession
from src.utils.schemas import CryptocurrencyListingsValidate

load_dotenv()


class CoinMarketCupAPI:
    __api_key = os.getenv("API_KEY_CMC")

    @classmethod
    async def get_cryptocurrency_listings(cls, limit: int = 1000):
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
