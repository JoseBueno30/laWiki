# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBool, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.id_ratings_body_v2 import IdRatingsBodyV2  # noqa: F401
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2  # noqa: F401


def test_assign_article_tags_v3(client: TestClient):
    """Test case for assign_article_tags_v3

    Assign Tags
    """
    id_tags_body_v2 = {"tag_ids":[{"id":"497f6eca-6276-4993-bfeb-53cbbbba6f08","tag":"string"}]}

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v3/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    json=id_tags_body_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_check_article_by_idv3(client: TestClient):
    """Test case for check_article_by_idv3

    Check Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/v3/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_articles_from_wiki_v3(client: TestClient):
    """Test case for delete_articles_from_wiki_v3

    Delete Articles from Wiki
    """

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v3/articles/wiki/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_article_tags_v3(client: TestClient):
    """Test case for unassign_article_tags_v3

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v3/articles/{id}/tags".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_rating_v3(client: TestClient):
    """Test case for update_rating_v3

    Update Rating
    """
    id_ratings_body_v2 = {"raitng":4.5}

    headers = {
        "user_id": 'user_id_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v3/articles/{id}/ratings".format(id='id_example'),
    #    headers=headers,
    #    json=id_ratings_body_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

