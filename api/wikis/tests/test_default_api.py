# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_wiki import NewWiki  # noqa: F401
from openapi_server.models.wiki import Wiki  # noqa: F401
from openapi_server.models.wiki_list import WikiList  # noqa: F401


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


def test_get_one_wiki_by_name(client: TestClient):
    """Test case for get_one_wiki_by_name

    Get Wiki by name
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/wikis/{name}".format(name='name_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki(client: TestClient):
    """Test case for get_wiki

    Get Wiki
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/wikis/{id}".format(id='id_example'),
    #    headers=headers,
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


def test_search_wikis(client: TestClient):
    """Test case for search_wikis

    Search for Wikis
    """
    params = [("name", 'name_example'),     ("offset", 20),     ("limit", 0),     ("order", '2013-10-20'),     ("creation_date", '2024/01/01, 2023/01/01-2024/01/01'),     ("author_name", 'author_name')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/wikis",
    #    headers=headers,
    #    params=params,
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

