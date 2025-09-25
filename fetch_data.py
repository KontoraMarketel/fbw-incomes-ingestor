import asyncio
import logging
from utils import get_yesterday_bounds_msk
import aiohttp


async def fetch_data(api_token: str, ts: str) -> str:
    url = "https://statistics-api.wildberries.ru/api/v1/supplier/incomes"
    headers = {"Authorization": api_token}
    all_incomes = []

    date_from, date_to = get_yesterday_bounds_msk(ts)

    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            params = {"dateFrom": str(date_from)}
            res = await fetch_page_with_retry(session, url, params)

            if not res:
                break

            all_incomes.extend(res)
            date_from = res[-1]["lastChangeDate"]

    return all_incomes


async def fetch_page_with_retry(session, url, params):
    while True:
        async with session.get(url, params=params) as response:
            if response.status == 429:
                retry_after = int(response.headers.get("X-Ratelimit-Retry", 10))
                logging.warning(
                    f"Rate limited (429). Retrying after {retry_after} seconds..."
                )
                await asyncio.sleep(retry_after)
                continue

            response.raise_for_status()
            return await response.json()
