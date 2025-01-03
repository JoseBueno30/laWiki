import httpx
import asyncio
import json
import os

COMMENTS_API_URL = os.getenv("COMMENTS_API_URL", "comments_api:8080")
WIKIS_API_URL = os.getenv("WIKIS_API_URL", "wikis_api:8084")
RATINGS_API_URL = os.getenv("RATINGS_API_URL", "ratings_api:8082")
LIBRETRANSLATE_API_URL = os.getenv("LIBRETRANSLATE_API_URL", "http://host.docker.internal:5000")
USERS_API_URL = os.getenv("USERS_API_URL", "users_api:8085")

async def get_user_comments(usr_id : str, order : str=None, limit : int=None, offset : int=None):
    async with httpx.AsyncClient() as client:
        query_params = {}
        if order:
            query_params['order'] = order
        if limit and limit != 20:
            query_params['limit'] = limit
        if offset and offset != 0:
            query_params['offset'] = offset

        comments_response = await client.get(f"http://{COMMENTS_API_URL}/v1/comments/users/{usr_id}",
                                              params=query_params)
        if comments_response.status_code != 200:
            raise Exception(comments_response.text)

        return comments_response.json()

async def get_wiki_author(wiki_id : str):
    async with httpx.AsyncClient() as client:
        wiki_response = await client.get(f"http://{WIKIS_API_URL}/v3/wikis/{wiki_id}", timeout=httpx.Timeout(200))
        if wiki_response.status_code != 200:
            raise Exception(wiki_response.text)

        return wiki_response.json()["author"]

async def check_if_wiki_exists(wiki_id : str):
    async with httpx.AsyncClient() as client:
        wiki_response = await client.head(f"http://{WIKIS_API_URL}/v3/wikis/{wiki_id}")
        return wiki_response.status_code == 200

async def check_if_tag_exists(tag_id : str):
    async with httpx.AsyncClient() as client:
        #   It's not implemented in tags api
        return True

async def delete_article_comments(article_id : str, user_id: str = None, admin: bool = None):
    headers = {}
    if admin and user_id:
        headers["user-id"] = user_id
        headers["admin"] = str(admin)
    print("ANTES DE BORRAR: ", headers)
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{COMMENTS_API_URL}/v2/comments/articles/{article_id}", timeout=httpx.Timeout(200), headers=headers)
        print("DESPUES DE BORRAR: ", delete_response)

        return delete_response.status_code == 204

async def delete_article_ratings(article_id : str, user_id: str = None, admin: bool = None):
    headers = {}
    if admin and user_id:
        headers["user-id"] = user_id
        headers["admin"] = str(admin)

    print("ANTES DE BORRAR")
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{RATINGS_API_URL}/v2/ratings/articles/{article_id}", timeout=httpx.Timeout(200), headers=headers)
        print("DESPUES DE BORRAR: ", delete_response)


        return delete_response

async def translate_body_to_lan(body, lan):
    async with httpx.AsyncClient() as client:
        body_params = {
            "q": body,
            "source": "auto",
            "target": lan,
            "format": "html"
        }
        translation = await client.post(f"{LIBRETRANSLATE_API_URL}/translate", params=body_params, timeout=httpx.Timeout(500))
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]

async def translate_text_to_lan(text, lan):
    async with httpx.AsyncClient() as client:
        text_params = {
            "q": text,
            "source": "auto",
            "target": lan,
            "format": "text"
        }
        print(f"{LIBRETRANSLATE_API_URL}/translate")
        translation = await client.post(f"{LIBRETRANSLATE_API_URL}/translate", params=text_params, timeout=httpx.Timeout(500))
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]

async def get_user(user_id : str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{USERS_API_URL}/v1/users/{user_id}", timeout=httpx.Timeout(200))

        if response.status_code == 401:
            raise HTTPException(status_code=403, detail="Forbidden")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Author not found")

        return response.json()