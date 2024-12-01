import httpx
from openapi_server.impl.misc import *
import json

LIBRETRANSLATE_URL = "host.docker.internal"
LIBRETRANSLATE_PORT = 5000
# LIBRETRANSLATE_URL = 'localhost'

def delete_articles_from_wiki(id_name : str):
    delete_articles_response = httpx.delete(HTTP_REQUEST_FORMAT.format(host=ARTICLES_ROUTE,port=ARTICLES_PORT,method=REMOVE_ALL_ARTICLES.format(id=id_name)))
    if delete_articles_response.status_code in range(400,500):
        raise LookupError("Could not delete articles, recieved " + str(delete_articles_response.status_code))
    elif delete_articles_response.status_code not in range(200,300):
        raise Exception("Could not delete articles, recieved " + str(delete_articles_response.status_code))
    
def delete_tags_from_wiki(id_name : str):
    url = HTTP_REQUEST_FORMAT.format(host=TAGS_ROUTE,port=TAGS_PORT,method=REMOVE_ALL_TAGS.format(id=id_name))
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
        translation = await client.post(f"http://{LIBRETRANSLATE_URL}:{LIBRETRANSLATE_PORT}/translate", params=body_params, timeout=httpx.Timeout(10))
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
        translation = await client.post(f"http://{LIBRETRANSLATE_URL}:{LIBRETRANSLATE_PORT}/translate", params=text_params, timeout=httpx.Timeout(10))
        translated_text = json.loads(translation.content.decode())
        return translated_text["translatedText"]