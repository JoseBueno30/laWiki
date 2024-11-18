# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.models_v2.article_v2 import ArticleV2  # noqa: F401
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2  # noqa: F401
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2  # noqa: F401
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2  # noqa: F401


def test_create_article_v2(client: TestClient):
    """Test case for create_article_v2

    Create Article
    """
    new_article_v2 = {"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","title":"title","body":"body","wiki_id":"wiki_id","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/articles",
    #    headers=headers,
    #    json=new_article_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_version_v2(client: TestClient):
    """Test case for create_article_version_v2

    Create ArticleVersion for an Article
    """
    new_article_version_v2 = {"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","title":"title","body":"body","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    json=new_article_version_v2,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_by_idv2(client: TestClient):
    """Test case for delete_article_by_idv2

    Delete Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_version_by_id_v2(client: TestClient):
    """Test case for delete_article_version_by_id_v2

    Delete ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_restore_article_version_v2(client: TestClient):
    """Test case for restore_article_version_v2

    Restore ArticleVersion
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/articles/{article_id}/versions/{version_id}".format(article_id='article_id_example', version_id='version_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

