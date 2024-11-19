import httpx

COMMENTS_PORT = 8080
COMMENTS_URL = "comments_api"

WIKI_PORT = 8084
WIKI_URL = "wikis_api"

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
        wiki_response = await client.head(f"http://{WIKI_URL}:{WIKI_PORT}/wikis/{wiki_id}")
        return wiki_response.status_code == 200

async def delete_article_comments(article_id : str):
    async with httpx.AsyncClient() as client:
        delete_response = await client.delete(f"http://{COMMENTS_URL}:{COMMENTS_PORT}/comments/articles/{article_id}")
        return delete_response.status_code == 204

async def translate_body_to_lan(body, lan):
    async with httpx.AsyncClient() as client:
        body_params = {
            "q": body,
            "source": "auto",
            "target": lan,
            "format": "html"
        }
        translation = await client.post("https://libretranslate.com/translate", params=body_params)
        return translation