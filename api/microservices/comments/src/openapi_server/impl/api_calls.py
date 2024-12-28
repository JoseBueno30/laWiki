import httpx
from fastapi import HTTPException
import os

ARTICLES_API_URL = os.getenv("ARTICLES_API_URL", "articles_api:8081")
USERS_API_URL = os.getenv("USERS_API_URL", "users_api:8085")

# This function is used to check if an article exists
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_API_URL}/v3/articles/{article_id}")
        return response.status_code == 200

async def get_article(article_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ARTICLES_API_URL}/v3/articles/{article_id}")
        return response.json()

async def check_user(user_id : str, user_email: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{USERS_API_URL}/v1/users/{user_id}?user_email={user_email}")
        return response.status_code

async def get_user(user_id : str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{USERS_API_URL}/v1/users/{user_id}")

        if response.status_code == 401:
            raise HTTPException(status_code=403, detail="Forbidden")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Author not found")

        return response.json()