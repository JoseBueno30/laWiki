# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.id_ratings_body import IdRatingsBody  # noqa: F401
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2  # noqa: F401


def test_assign_wiki_tags_v2(client: TestClient):
    """Test case for assign_wiki_tags_v2

    Assign Tags
    """
    id_tags_body_v2 = {"tag_ids":[{"id":"1","name":{"en":"Gift Cards","es":"Tarjetas de regalo"},"wiki_id":"1"},{"id":"2","name":{"en":"Stores","es":"Tiendas"},"wiki_id":"1"},{"id":"1","name":{"en":"Sports cars","es":"Coches deportivo"},"wiki_id":"2"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/wikis/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    json=id_tags_body_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_check_wiki_by_idv2(client: TestClient):
    """Test case for check_wiki_by_idv2

    Check Wiki
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_wiki_tags_v2(client: TestClient):
    """Test case for unassign_wiki_tags_v2

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/wikis/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_rating_v2(client: TestClient):
    """Test case for update_rating_v2

    Update Rating
    """
    id_ratings_body = {"rating":4.5}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/wikis/{id}/ratings".format(id='id_example'),
    #    headers=headers,
    #    json=id_ratings_body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

