import httpx
from fastapi import HTTPException

COMMENTS_PORT = 8080
COMMENTS_URL = "http://comments_api:" + str(COMMENTS_PORT)

ARTICLES_PORT = 8081
ARTICLES_URL = "http://articles_api:" + str(ARTICLES_PORT)

RATINGS_PORT = 8082
RATINGS_URL = "http://ratings_api:" + str(RATINGS_PORT)

TAGS_PORT = 8083
TAGS_URL = "http://tags_api:" + str(TAGS_PORT)

WIKIS_PORT = 8084
WIKIS_URL = "http://wikis_api:" + str(WIKIS_PORT)

USERS_PORT = 8085
USERS_URL = "http://users_api:" + str(USERS_PORT)

async def forward_request(method: str, url: str, query_params: dict = None, json: dict = None, headers_params: dict = None, content: bytes = None):
    params = None
    headers = None

    if query_params is not None:
        params = {key: value for key, value in query_params.items() if value is not None}
    if headers_params is not None:
        headers = {key: value for key, value in headers_params.items() if value is not None}

    async with httpx.AsyncClient() as client:
        response = await client.request(method = method, url = url, params = params, headers = headers, json = json, content = content, timeout=httpx.Timeout(180))

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()