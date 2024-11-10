from typing import List

import httpx

ARTICLES_PORT = 8081
# ARTICLES_URL = "articles_api"
ARTICLES_URL = "localhost"

WIKIS_PORT = 8082
# WIKIS_URL = "articles_api"
WIKIS_URL = "localhost"


"""if not await api_calls.check_article(article_id):
            raise Exception("Article not found")"""

# Article microservice api calls
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{article_id}")
        return response.status_code == 200

async def get_article(article_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{article_id}")
        return response.json()

async def assign_article_tags(article_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{article_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_article_tags(article_id: str, ids: List[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{article_id}/tags",
                                     params=params)
        return response.status_code == 200

# Wiki microservice api calls
async def check_wiki(wiki_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{WIKIS_URL}:{WIKIS_PORT}/wikis/{wiki_id}")
        return response.status_code == 200

async def assign_wiki_tags(wiki_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{WIKIS_URL}:{WIKIS_PORT}/wikis/{wiki_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_wiki_tags(wiki_id: str, ids: list[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{WIKIS_URL}:{WIKIS_PORT}/wikis/{wiki_id}/tags",
                                       params=params)
        return response.status_code == 200