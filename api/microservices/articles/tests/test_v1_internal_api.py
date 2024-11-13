# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.id_ratings_body_v1 import IdRatingsBodyV1  # noqa: F401
from openapi_server.models.id_tags_body_v1 import IdTagsBodyV1  # noqa: F401


def test_assign_article_tags_v1(client: TestClient):
    """Test case for assign_article_tags_v1

    Assign Tags
    """
    id_tags_body_v1 = {"tag_ids":[{"id":"497f6eca-6276-4993-bfeb-53cbbbba6f08","tag":"string"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    json=id_tags_body_v1,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_check_article_by_idv1(client: TestClient):
    """Test case for check_article_by_idv1

    Check Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/v1/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_article_tags_v1(client: TestClient):
    """Test case for unassign_article_tags_v1

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_rating_v1(client: TestClient):
    """Test case for update_rating_v1

    Update Rating
    """
    id_ratings_body_v1 = {"raitng":4.5}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/articles/{id}/ratings".format(id='id_example'),
    #    headers=headers,
    #    json=id_ratings_body_v1,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

