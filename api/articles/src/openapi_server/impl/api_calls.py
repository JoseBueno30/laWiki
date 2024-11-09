import httpx

COMMENTS_PORT = 8081
COMMENTS_URL = "localhost"

WIKI_PORT = 8081
WIKI_URL = "localhost"

async def get_user_comments(usr_id : str, order : str="recent", limit : int=20, offset : int=0):
    async with httpx.AsyncClient() as client:
        query_params = {
            "order": order,
            "limit": limit,
            "offset": offset
        }
        comments_response = await client.get(f"http://{COMMENTS_URL}:{COMMENTS_PORT}/comments/users/{usr_id}",
                                              params=query_params)
        return comments_response


async def check_if_wiki_exists(wiki_id : str):
    async with httpx.AsyncClient() as client:
        wiki_response = await client.head(f"http://{WIKI_URL}:{WIKI_PORT}/wikis/{wiki_id}")
        return wiki_response.status_code == 200