from datetime import datetime, timedelta

import aiohttp
import json


# <ts> это дата когда выполняется функция, найди от нее вчерашнюю дату и используй
async def fetch_data(api_token: str, ts: str) -> str:
    url = "https://statistics-api.wildberries.ru/api/v1/supplier/incomes"
    headers = {"Authorization": api_token}

    all_incomes = []

    dt_ts = datetime.fromisoformat(ts)
    yesterday = (dt_ts - timedelta(days=1)).strftime("%Y-%m-%d")

    datefrom = yesterday

    async with aiohttp.ClientSession() as session:
        while True:
            params = {"dateFrom": datefrom}
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                res = await response.json()

                if not res:
                    break

                all_incomes.extend(res)
                datefrom = res[-1]["lastChangeDate"]

    return json.dumps(all_incomes, indent=2, ensure_ascii=False)
