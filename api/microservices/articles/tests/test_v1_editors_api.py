# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.article_v1 import ArticleV1  # noqa: F401
from openapi_server.models.article_version_v1 import ArticleVersionV1  # noqa: F401
from openapi_server.models.new_article_v1 import NewArticleV1  # noqa: F401
from openapi_server.models.new_article_version_v1 import NewArticleVersionV1  # noqa: F401


def test_create_article_v1(client: TestClient):
    """Test case for create_article_v1

    Create Article
    """
    new_article_v1 = {"author":{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"title":"title","body":"body","wiki_id":"wiki_id","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/articles",
    #    headers=headers,
    #    json=new_article_v1,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_version_v1(client: TestClient):
    """Test case for create_article_version_v1

    Create ArticleVersion for an Article
    """
    new_article_version_v1 = {"author":{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"title":"title","body":"body","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"tag"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    json=new_article_version_v1,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_by_idv1(client: TestClient):
    """Test case for delete_article_by_idv1

    Delete Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_version_by_id_v1(client: TestClient):
    """Test case for delete_article_version_by_id_v1

    Delete ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_restore_article_version_v1(client: TestClient):
    """Test case for restore_article_version_v1

    Restore ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/articles/{article_id}/versions/{version_id}".format(article_id='article_id_example', version_id='version_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

