# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_tag import NewTag  # noqa: F401
from openapi_server.models.tag import Tag  # noqa: F401
from openapi_server.models.tag_id_list import TagIDList  # noqa: F401
from openapi_server.models.tag_list import TagList  # noqa: F401


def test_assign_tags(client: TestClient):
    """Test case for assign_tags

    Assign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_tag(client: TestClient):
    """Test case for delete_tag

    Delete Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_articles_tags(client: TestClient):
    """Test case for get_articles_tags

    Get Articles Tag
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_tag(client: TestClient):
    """Test case for get_tag

    Get Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_tags(client: TestClient):
    """Test case for get_wiki_tags

    Get Wikis Tags
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_wiki_tag(client: TestClient):
    """Test case for post_wiki_tag

    Create Tag
    """
    new_tag = {"tag":"tag"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_tag,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_tags(client: TestClient):
    """Test case for unassign_tags

    Unassign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

