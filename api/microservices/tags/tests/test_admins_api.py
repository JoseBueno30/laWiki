# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_tag import NewTag  # noqa: F401
from openapi_server.models.tag import Tag  # noqa: F401


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

