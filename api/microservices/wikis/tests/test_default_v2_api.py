# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_wiki_v2 import NewWikiV2  # noqa: F401
from openapi_server.models.wiki_list_v2 import WikiListV2  # noqa: F401
from openapi_server.models.wiki_v2 import WikiV2  # noqa: F401


def test_create_wiki_v2(client: TestClient):
    """Test case for create_wiki_v2

    Create Wiki
    """
    new_wiki_v2 = {"image":"https://openapi-generator.tech","author":"author","name":[{"en":"Wiki name","es":"Nombre de wiki"}],"description":"description","lang":"lang"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/wikis",
    #    headers=headers,
    #    json=new_wiki_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_v2(client: TestClient):
    """Test case for get_wiki_v2

    Get Wiki
    """
    params = [("lang", 'lang_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_wikis_v2(client: TestClient):
    """Test case for search_wikis_v2

    Search for Wikis
    """
    params = [("name", 'name_example'),     ("offset", 20),     ("limit", 0),     ("order", '2013-10-20'),     ("creation_date", '2024/01/01, 2023/01/01-2024/01/01'),     ("author_name", 'author_name')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/wikis",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

