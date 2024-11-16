# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2  # noqa: F401
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2  # noqa: F401


def test_assign_article_tags_v2(client: TestClient):
    """Test case for assign_article_tags_v2

    Assign Tags
    """
    id_tags_body_v2 = {"tag_ids":[{"id":"497f6eca-6276-4993-bfeb-53cbbbba6f08","tag":"string"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    json=id_tags_body_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_check_article_by_idv2(client: TestClient):
    """Test case for check_article_by_idv2

    Check Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/v2/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_article_tags_v2(client: TestClient):
    """Test case for unassign_article_tags_v2

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_rating_v2(client: TestClient):
    """Test case for update_rating_v2

    Update Rating
    """
    id_ratings_body_v2 = {"raitng":4.5}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/articles/{id}/ratings".format(id='id_example'),
    #    headers=headers,
    #    json=id_ratings_body_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

