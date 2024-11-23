import httpx
from openapi_server.impl.misc import *

def delete_articles_from_wiki(id_name : str):
    delete_articles_response = httpx.delete(HTTP_REQUEST_FORMAT.format(host=ARTICLES_ROUTE,port=ARTICLES_PORT,method=REMOVE_ALL_ARTICLES.format(id=id_name)))
    if delete_articles_response.status_code in range(400,500):
        raise LookupError()
    elif delete_articles_response.status_code not in range(200,300):
        raise Exception()