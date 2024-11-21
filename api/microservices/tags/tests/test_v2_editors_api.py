# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_tag_v2 import NewTagV2  # noqa: F401
from openapi_server.models.tag_id_list import TagIDList  # noqa: F401
from openapi_server.models.tag_v2 import TagV2  # noqa: F401


def test_assign_tags_v2(client: TestClient):
    """Test case for assign_tags_v2

    Assign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_tag_v2(client: TestClient):
    """Test case for delete_tag_v2

    Delete Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_wiki_tag_v2(client: TestClient):
    """Test case for post_wiki_tag_v2

    Create Tag
    """
    new_tag_v2 = {"translation":1,"language":"language","tag":"tag"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_tag_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_tags_v2(client: TestClient):
    """Test case for unassign_tags_v2

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200
