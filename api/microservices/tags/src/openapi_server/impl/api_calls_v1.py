from typing import List

import httpx

import os

ARTICLES_API_URL = os.getenv("ARTICLES_API_URL", "articles_api:8081")
WIKIS_API_URL = os.getenv("WIKIS_API_URL", "wikis_api:8084")


# Article microservice api calls
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_API_URL}/v1/articles/{article_id}")
        return response.status_code == 200

async def get_article(article_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ARTICLES_API_URL}/v1/articles/{article_id}")
        return response.json()

async def assign_article_tags(article_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{ARTICLES_API_URL}/v1/articles/{article_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_article_tags(article_id: str, ids: List[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{ARTICLES_API_URL}/v1/articles/{article_id}/tags",
                                       params=params)
        return response.status_code == 200

# Wiki microservice api calls
async def check_wiki(wiki_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{WIKIS_API_URL}/v1/wikis/{wiki_id}")
        return response.status_code == 200

async def assign_wiki_tags(wiki_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{WIKIS_API_URL}/v1/wikis/{wiki_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_wiki_tags(wiki_id: str, ids: List[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{WIKIS_API_URL}/v1/wikis/{wiki_id}/tags",
                                       params=params)
        return response.status_code == 200