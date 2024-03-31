import aiohttp


class AsyncSession:
    @staticmethod
    async def get(url, headers, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.text()
