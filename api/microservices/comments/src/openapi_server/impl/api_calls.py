import httpx
from fastapi import HTTPException

ARTICLES_PORT = 8081
ARTICLES_URL = "articles_api"
# ARTICLES_URL = "localhost"

USERS_PORT = 8085
USERS_URL = "users_api"

# This function is used to check if an article exists
async def check_article(article_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/v2/articles/{article_id}")
        return response.status_code == 200

async def check_user(user_id : str, user_email: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.head(f"http://{USERS_URL}:{USERS_PORT}/v1/users/{user_id}?user_email={user_email}")
        return response.status_code

async def get_user(user_id: str, user_email : str, admin : bool) -> dict:
    async with httpx.AsyncClient() as client:
        headers = {
            "user-email": user_email,
            "admin": str(admin)
        }
        response = await client.get(f"http://{USERS_URL}:{USERS_PORT}/v1/users/{user_id}", headers=headers)

        if response.status_code == 401:
            raise HTTPException(status_code=403, detail="Forbidden")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Author not found")

        return response.json()