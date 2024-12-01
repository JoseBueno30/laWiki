from typing import List

import httpx

ARTICLES_PORT = 8081
ARTICLES_URL = "articles_api"
#ARTICLES_URL = "localhost"

WIKIS_PORT = 8084
WIKIS_URL = "wikis_api"
#WIKIS_URL = "localhost"

TRANSLATION_PORT = 5000
TRANSLATION_URL = "host.docker.internal"
#TRANSLATION_URL = "localhost"


# Article microservice api calls
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/v2/articles/{article_id}")
        return response.status_code == 200

async def get_article(article_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/v2/articles/{article_id}")
        return response.json()

async def assign_article_tags(article_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/v2/articles/{article_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_article_tags(article_id: str, ids: List[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/v2/articles/{article_id}/tags",
                                     params=params)
        return response.status_code == 200

# Wiki microservice api calls
async def check_wiki(wiki_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{WIKIS_URL}:{WIKIS_PORT}/v2/wikis/{wiki_id}")
        return response.status_code == 200

async def assign_wiki_tags(wiki_id: str, id_tags_body) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://{WIKIS_URL}:{WIKIS_PORT}/v2/wikis/{wiki_id}/tags",
                                    json=id_tags_body)
        return response.status_code == 200

async def unassign_wiki_tags(wiki_id: str, ids: List[str]) -> bool:
    async with httpx.AsyncClient() as client:
        params = {"ids" : ids}
        response = await client.delete(f"http://{WIKIS_URL}:{WIKIS_PORT}/v2/wikis/{wiki_id}/tags",
                                       params=params)
        return response.status_code == 200

# Translation microservice api calls
async def translate(text: str, source: str, target: str) -> str:
    data = {
        "q": text,
        "source": source,
        "target": target
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{TRANSLATION_URL}:{TRANSLATION_PORT}/translate",
            data=data
        )

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"Error while translating: {response.status_code} {response.text}")
