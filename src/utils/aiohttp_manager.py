import aiohttp


class AsyncSession:
    @staticmethod
    async def get(url, headers, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.text()

    @staticmethod
    async def post(url, headers, params, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, params=params, json=data
            ) as response:
                response.raise_for_status()
                return await response.text()
