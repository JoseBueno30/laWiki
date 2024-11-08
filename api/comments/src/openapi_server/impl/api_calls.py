import httpx

ARTICLES_PORT = 8081
ARTICLES_URL = "articles_api"

# This function is used to check if an article exists
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{article_id}")
        return response.status_code == 200