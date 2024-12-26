import os
from typing import Union

import httpx
from fastapi import HTTPException

COMMENTS_API_URL = os.getenv("COMMENTS_API_URL", "http://comments_api:8080")
ARTICLES_API_URL = os.getenv("ARTICLES_API_URL", "http://articles_api:8081")
RATINGS_API_URL = os.getenv("RATINGS_API_URL", "http://ratings_api:8082")
TAGS_API_URL = os.getenv("TAGS_API_URL", "http://tags_api:8083")
WIKIS_API_URL = os.getenv("WIKIS_API_URL", "http://wikis_api:8084")
USERS_API_URL = os.getenv("USERS_API_URL", "http://users_api:8085")

async def forward_request(method: str, url: str, query_params: dict = None, json: Union[str,dict] = None, headers_params: dict = None, content: bytes = None):
    params = None
    headers = None

    if query_params is not None:
        params = {key: value for key, value in query_params.items() if value is not None}
    if headers_params is not None:
        headers = {key: value for key, value in headers_params.items() if value is not None}

    async with httpx.AsyncClient() as client:
        response = await client.request(method = method, url = url, params = params, headers = headers, json = json, content = content, timeout=httpx.Timeout(180))

        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response["detail"])

        return response.json()