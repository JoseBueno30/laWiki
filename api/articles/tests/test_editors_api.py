# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.article import Article  # noqa: F401
from openapi_server.models.article_version import ArticleVersion  # noqa: F401
from openapi_server.models.new_article import NewArticle  # noqa: F401
from openapi_server.models.new_article_version import NewArticleVersion  # noqa: F401


def test_create_article(client: TestClient):
    """Test case for create_article

    Create Article
    """
    new_article = {"author":{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"title":"title","body":"body","wiki_id":"wiki_id","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/articles",
    #    headers=headers,
    #    json=new_article,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_version(client: TestClient):
    """Test case for create_article_version

    Create ArticleVersion for an Article
    """
    new_article_version = {"author":{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"title":"title","body":"body","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    json=new_article_version,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_by_id(client: TestClient):
    """Test case for delete_article_by_id

    Delete Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_version_by_id(client: TestClient):
    """Test case for delete_article_version_by_id

    Delete ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_restore_article_version(client: TestClient):
    """Test case for restore_article_version

    Restore ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/articles/{article_id}/versions/{version_id}".format(article_id='article_id_example', version_id='version_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

