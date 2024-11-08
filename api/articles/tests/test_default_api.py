# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.article import Article  # noqa: F401
from openapi_server.models.article_list import ArticleList  # noqa: F401
from openapi_server.models.article_version import ArticleVersion  # noqa: F401
from openapi_server.models.article_version_list import ArticleVersionList  # noqa: F401


def test_get_article_by_author(client: TestClient):
    """Test case for get_article_by_author

    Get Articles by Author
    """
    params = [("offset", 0),     ("limit", 0),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/author/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_id(client: TestClient):
    """Test case for get_article_by_id

    Get Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_name(client: TestClient):
    """Test case for get_article_by_name

    Get ArticleVersion by name
    """
    params = [("wiki", 'wiki_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/versions/by-name/{name}".format(name='name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_by_id(client: TestClient):
    """Test case for get_article_version_by_id

    Get ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_list_by_article_id(client: TestClient):
    """Test case for get_article_version_list_by_article_id

    Get Article's ArticleVersions
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_articles_commented_by_user(client: TestClient):
    """Test case for get_articles_commented_by_user

    Get Articles commented by User
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'recent, oldest')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles/commented_by/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_articles(client: TestClient):
    """Test case for search_articles

    Search for Articles
    """
    params = [("wiki_id", 'wiki_id_example'),     ("name", 'name'),     ("tags", ['[\"tag1\",\"tag2\"]']),     ("offset", 0),     ("limit", 20),     ("order", 'none'),     ("creation_date", '2013-10-20'),     ("author_name", 'author_name_example'),     ("editor_name", 'editor_name_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/articles",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

