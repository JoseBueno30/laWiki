import httpx
import json

COMMENTS_PORT = 8080
COMMENTS_URL = "comments_api"

WIKI_PORT = 8084
WIKI_URL = "wikis_api"

RATINGS_PORT = 8082
RATINGS_URL = "ratings_api"

LIBRETRANSLATE_URL = "host.docker.internal"
LIBRETRANSLATE_PORT = 5000

async def get_user_comments(usr_id : str, order : str=None, limit : int=None, offset : int=None):
    async with httpx.AsyncClient() as client:
        query_params = {}
        if order:
            query_params['order'] = order
        if limit and limit != 20:
            query_params['limit'] = limit
        if offset and offset != 0:
            query_params['offset'] = offset

        comments_response = await client.get(f"http://{COMMENTS_URL}:{COMMENTS_PORT}/comments/users/{usr_id}",
                                              params=query_params)
        if comments_response.status_code != 200:
            raise Exception(comments_response.text)

        return comments_response.json()


async def check_if_wiki_exists(wiki_id : str):
    async with httpx.AsyncClient() as client:
        wiki_response = await client.head(f"http://{WIKI_URL}:{WIKI_PORT}/v2/wikis/{wiki_id}")
        return wiki_response.status_code == 200

async def check_if_tag_exists(tag_id : str):
    async with httpx.AsyncClient() as client:
        #   It's not implemented in tags api
        return True

async def delete_article_comments(article_id : str):
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{COMMENTS_URL}:{COMMENTS_PORT}/comments/articles/{article_id}")
        return delete_response.status_code == 204

async def delete_article_ratings(article_id : str):
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{RATINGS_URL}:{RATINGS_PORT}/ratings/articles/{article_id}")
        return delete_response.status_code == 204

async def translate_body_to_lan(body, lan):
    async with httpx.AsyncClient() as client:
        body_params = {
            "q": body,
            "source": "auto",
            "target": lan,
            "format": "html"
        }
        translation = await client.post(f"http://{LIBRETRANSLATE_URL}:{LIBRETRANSLATE_PORT}/translate", params=body_params, timeout=httpx.Timeout(180))
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
        translation = await client.post(f"http://{LIBRETRANSLATE_URL}:{LIBRETRANSLATE_PORT}/translate", params=text_params)
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]