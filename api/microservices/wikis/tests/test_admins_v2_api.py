# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_wiki_v2 import NewWikiV2  # noqa: F401
from openapi_server.models.wiki_v2 import WikiV2  # noqa: F401


def test_remove_wiki_v2(client: TestClient):
    """Test case for remove_wiki_v2

    Remove Wiki
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_wiki_v2(client: TestClient):
    """Test case for update_wiki_v2

    Update Wiki
    """
    new_wiki_v2 = {"image":"https://openapi-generator.tech","author":"author","name":[{"en":"Wiki name","es":"Nombre de wiki"}],"description":"description","lang":"lang"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #    json=new_wiki_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

