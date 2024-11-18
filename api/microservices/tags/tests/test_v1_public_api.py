# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.tag import Tag  # noqa: F401
from openapi_server.models.tag_list import TagList  # noqa: F401


def test_get_articles_tags_v1(client: TestClient):
    """Test case for get_articles_tags_v1

    Get Articles Tag
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_tag_v1(client: TestClient):
    """Test case for get_tag_v1

    Get Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_tags_v1(client: TestClient):
    """Test case for get_wiki_tags_v1

    Get Wikis Tags
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

