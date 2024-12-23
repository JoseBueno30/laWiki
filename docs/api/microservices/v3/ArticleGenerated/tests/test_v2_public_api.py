# coding: utf-8

from fastapi.testclient import TestClient


from datetime import date  # noqa: F401
from pydantic import Field, StrictBool, StrictInt, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.article_list_v2 import ArticleListV2  # noqa: F401
from openapi_server.models.article_v2 import ArticleV2  # noqa: F401
from openapi_server.models.article_version_list_v2 import ArticleVersionListV2  # noqa: F401
from openapi_server.models.article_version_v2 import ArticleVersionV2  # noqa: F401
from openapi_server.models.inline_response200_v2 import InlineResponse200V2  # noqa: F401


def test_get_article_by_author_v2(client: TestClient):
    """Test case for get_article_by_author_v2

    Get Articles by Author
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/author/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_id_v2(client: TestClient):
    """Test case for get_article_by_id_v2

    Get Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_name_v2(client: TestClient):
    """Test case for get_article_by_name_v2

    Get ArticleVersion by name
    """
    params = [("wiki", 'wiki_example'),     ("lan", 'lan_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/versions/by-name/{name}".format(name='name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_body_by_idv2(client: TestClient):
    """Test case for get_article_version_body_by_idv2

    Get ArticleVersion body
    """
    params = [("parsed", False),     ("lan", 'lan_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/versions/{id}/body".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_by_id_v2(client: TestClient):
    """Test case for get_article_version_by_id_v2

    Get ArticleVersion
    """
    params = [("lan", 'lan_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_list_by_article_idv2(client: TestClient):
    """Test case for get_article_version_list_by_article_idv2

    Get Article's ArticleVersions
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_articles_commented_by_user_v2(client: TestClient):
    """Test case for get_articles_commented_by_user_v2

    Get Articles commented by User
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles/commented_by/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_articles_v2(client: TestClient):
    """Test case for search_articles_v2

    Search for Articles
    """
    params = [("wiki_id", 'wiki_id_example'),     ("name", 'name'),     ("tags", ['[\"tag1\",\"tag2\"]']),     ("offset", 0),     ("limit", 20),     ("order", 'none'),     ("creation_date", '2013-10-20'),     ("author_name", 'author_name_example'),     ("editor_name", 'editor_name_example'),     ("lan", 'lan_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/articles",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

