from app.configs.google_api_config import GOOGLE_OPENSEARCH_API_KEY,GOOGLE_OPENSEARCH_CX_KEY
from .import httpx,ic

async def google_image_search(query: str):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_OPENSEARCH_API_KEY,
        "cx": GOOGLE_OPENSEARCH_CX_KEY,
        "q": query,
        "searchType": "image",
        "num": 4
    }

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.get(url, params=params)
        data = response.json()

        try:
            return [item["link"] for item in data.get("items", [])][:4]
        except:
            return []