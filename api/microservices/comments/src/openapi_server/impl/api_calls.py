import httpx
import os

ARTICLES_API_URL = os.getenv("ARTICLES_API_URL", "articles_api:8081")


# This function is used to check if an article exists
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_API_URL}/v2/articles/{article_id}")
        return response.status_code == 200