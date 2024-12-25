import httpx
import json
import os

COMMENTS_API_URL = os.getenv("COMMENTS_API_URL", "comments_api:8080")
WIKIS_API_URL = os.getenv("WIKIS_API_URL", "wikis_api:8084")
RATINGS_API_URL = os.getenv("RATINGS_API_URL", "ratings_api:8082")
LIBRETRANSLATE_API_URL = os.getenv("LIBRETRANSALTE_API_URL", "host.docker.internal:5000")

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


async def check_if_wiki_exists(wiki_id : str):
    async with httpx.AsyncClient() as client:
        wiki_response = await client.head(f"http://{WIKIS_API_URL}/v2/wikis/{wiki_id}")
        return wiki_response.status_code == 200

async def check_if_tag_exists(tag_id : str):
    async with httpx.AsyncClient() as client:
        #   It's not implemented in tags api
        return True

async def delete_article_comments(article_id : str):
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{COMMENTS_API_URL}/v1/comments/articles/{article_id}")
        return delete_response.status_code == 204

async def delete_article_ratings(article_id : str):
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{RATINGS_API_URL}/ratings/articles/{article_id}")
        return delete_response.status_code == 204

async def translate_body_to_lan(body, lan):
    async with httpx.AsyncClient() as client:
        body_params = {
            "q": body,
            "source": "auto",
            "target": lan,
            "format": "html"
        }
        translation = await client.post(f"http://{LIBRETRANSLATE_API_URL}/translate", params=body_params, timeout=httpx.Timeout(500))
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
        translation = await client.post(f"http://{LIBRETRANSLATE_API_URL}/translate", params=text_params)
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]