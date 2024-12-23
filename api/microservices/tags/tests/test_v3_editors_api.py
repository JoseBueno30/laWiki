# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_tag_v2 import NewTagV2  # noqa: F401
from openapi_server.models.tag_id_list import TagIDList  # noqa: F401
from openapi_server.models.tag_v2 import TagV2  # noqa: F401


def test_assign_tags_v3(client: TestClient):
    """Test case for assign_tags_v3

    Assign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v3/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_tag_v3(client: TestClient):
    """Test case for delete_tag_v3

    Delete Tag
    """

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v3/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_wiki_tag_v3(client: TestClient):
    """Test case for post_wiki_tag_v3

    Create Tag
    """
    new_tag_v2 = {"translation":1,"language":"language","tag":"tag"}

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v3/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_tag_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_tags_v3(client: TestClient):
    """Test case for unassign_tags_v3

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
        "user_id": 'user_id_example',
        "admin": 'admin_example',
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v3/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

