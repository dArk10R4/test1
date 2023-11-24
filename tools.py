import aiohttp

from environment import get_env


async def internet_search_with_bing(query: str) -> str:
    endpoint = get_env('BING_SEARCH_V7_ENDPOINT') + "/v7.0/search"
    headers = {'Ocp-Apim-Subscription-Key': get_env("BING_SEARCH_V7_SUBSCRIPTION_KEY")}
    params = {"q": query, "mkt": "en-US"}

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, headers=headers, params=params) as response:
            response = await response.json()
            text = ""
            for index, r in enumerate(response["webPages"]["value"]):
                if index == 5:
                    break
                text += r["snippet"] + "\n"
            return text
        