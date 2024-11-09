# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_wiki import NewWiki  # noqa: F401
from openapi_server.models.wiki import Wiki  # noqa: F401


def test_create_wiki(client: TestClient):
    """Test case for create_wiki

    Create Wiki
    """
    new_wiki = {"author":"author","name":"name","description":"description"}
    params = [("name", 'name_example'),     ("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/wikis",
    #    headers=headers,
    #    json=new_wiki,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_remove_wiki(client: TestClient):
    """Test case for remove_wiki

    Remove Wiki
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_wiki(client: TestClient):
    """Test case for update_wiki

    Update Wiki
    """
    new_wiki = {"author":"author","name":"name","description":"description"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_wiki,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

