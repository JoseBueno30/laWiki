import httpx
from openapi_server.impl.misc import *
import json
import os

LIBRETRANSLATE_API_URL = os.getenv("LIBRETRANSLATE_API_URL", "http://host.docker.internal:5000")
ARTICLES_API_URL = os.getenv("ARTICLES_API_URL", "articles_api:8081")
TAGS_API_URL = os.getenv("TAGS_API_URL", "tags_api:8083")
USERS_API_URL = os.getenv("USERS_API_URL", "users_api:8085")

def get_user_by_id(user_id : str):
    user_response = httpx.get(HTTP_REQUEST_FORMAT.format(url=USERS_API_URL,method=GET_USER_BY_ID.format(id=user_id)))
    if user_response.status_code == 404:
        raise LookupError("User not found")
    elif user_response.status_code not in range(200,300):
        raise Exception("Could not get user, recieved " + str(user_response.status_code))
    return user_response.json()


def delete_articles_from_wiki(id_name : str, user_id : str, admin : bool):
    headers = {}
    if user_id and admin is not None:
        headers = {"user-id": user_id, "admin": str(admin)}
        # print(headers)
    delete_articles_response = (
        httpx.delete(HTTP_REQUEST_FORMAT.format(url=ARTICLES_API_URL,
                                                method=REMOVE_ALL_ARTICLES.format(id=id_name)),
                                            headers=headers,timeout=httpx.Timeout(500)))

    if delete_articles_response.status_code in range(400,500):
        raise LookupError("Could not delete articles, recieved " + str(delete_articles_response.status_code))
    elif delete_articles_response.status_code not in range(200,300):
        raise Exception("Could not delete articles, recieved " + str(delete_articles_response.status_code))
    
def delete_tags_from_wiki(id_name : str):
    url = HTTP_REQUEST_FORMAT.format(url=TAGS_API_URL,method=REMOVE_ALL_TAGS.format(id=id_name))
    print(url)
    delete_tags_response = httpx.delete(url)
    if delete_tags_response.status_code in range(400,500):
        raise LookupError("Could not delete tags, recieved " + str(delete_tags_response.status_code))
    elif delete_tags_response.status_code not in range(200,300):
        raise Exception("Could not delete tags, recieved " + str(delete_tags_response.status_code))
    
async def translate_body_to_lan(body, lan):
    async with httpx.AsyncClient() as client:
        body_params = {
            "q": body,
            "source": "auto",
            "target": lan,
            "format": "html"
        }
        translation = await client.post(f"{LIBRETRANSLATE_API_URL}/translate", params=body_params, timeout=httpx.Timeout(10))
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
        translation = await client.post(f"{LIBRETRANSLATE_API_URL}/translate", params=text_params, timeout=httpx.Timeout(10))
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]