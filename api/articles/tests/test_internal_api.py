# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.id_ratings_body import IdRatingsBody  # noqa: F401
from openapi_server.models.id_tags_body import IdTagsBody  # noqa: F401


def test_assign_article_tags(client: TestClient):
    """Test case for assign_article_tags

    Assign Tags
    """
    id_tags_body = {"tag_ids":[{"id":"497f6eca-6276-4993-bfeb-53cbbbba6f08","tag":"string"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    json=id_tags_body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_check_article_by_id(client: TestClient):
    """Test case for check_article_by_id

    Check Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_article_tags(client: TestClient):
    """Test case for unassign_article_tags

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_rating(client: TestClient):
    """Test case for update_rating

    Update Rating
    """
    id_ratings_body = {"raitng":4.5}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/articles/{id}/ratings".format(id='id_example'),
    #    headers=headers,
    #    json=id_ratings_body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

