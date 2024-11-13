# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.article_list_v1 import ArticleListV1  # noqa: F401
from openapi_server.models.article_v1 import ArticleV1  # noqa: F401
from openapi_server.models.article_version_list_v1 import ArticleVersionListV1  # noqa: F401
from openapi_server.models.article_version_v1 import ArticleVersionV1  # noqa: F401


def test_get_article_by_author_v1(client: TestClient):
    """Test case for get_article_by_author_v1

    Get Articles by Author
    """
    params = [("offset", 0),     ("limit", 0),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/author/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_id_v1(client: TestClient):
    """Test case for get_article_by_id_v1

    Get Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_name_v1(client: TestClient):
    """Test case for get_article_by_name_v1

    Get ArticleVersion by name
    """
    params = [("wiki", 'wiki_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/versions/by-name/{name}".format(name='name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_by_id_v1(client: TestClient):
    """Test case for get_article_version_by_id_v1

    Get ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_list_by_article_idv1(client: TestClient):
    """Test case for get_article_version_list_by_article_idv1

    Get Article's ArticleVersions
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_articles_commented_by_user_v1(client: TestClient):
    """Test case for get_articles_commented_by_user_v1

    Get Articles commented by User
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/commented_by/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_articles_v1(client: TestClient):
    """Test case for search_articles_v1

    Search for Articles
    """
    params = [("wiki_id", 'wiki_id_example'),     ("name", 'name'),     ("tags", ['[\"tag1\",\"tag2\"]']),     ("offset", 0),     ("limit", 20),     ("order", 'none'),     ("creation_date", '2013-10-20'),     ("author_name", 'author_name_example'),     ("editor_name", 'editor_name_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

