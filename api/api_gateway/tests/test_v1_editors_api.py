# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.article import Article  # noqa: F401
from openapi_server.models.article_version import ArticleVersion  # noqa: F401
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: F401
from openapi_server.models.new_article import NewArticle  # noqa: F401
from openapi_server.models.new_article_version import NewArticleVersion  # noqa: F401
from openapi_server.models.tag_id_list import TagIDList  # noqa: F401


def test_assign_tags(client: TestClient):
    """Test case for assign_tags

    Assign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article(client: TestClient):
    """Test case for create_article

    Create Article
    """
    new_article = {"trasnlate_title":1,"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","title":"title","body":"body","wiki_id":"wiki_id","tags":[{"translations":{"key":"translations"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","wiki_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","articles":[{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"}]},{"translations":{"key":"translations"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","wiki_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","articles":[{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"}]}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/articles",
    #    headers=headers,
    #    json=new_article,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_version(client: TestClient):
    """Test case for create_article_version

    Create ArticleVersion for an Article
    """
    new_article_version = {"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","translate_title":1,"title":"title","body":"body","tags":[{"translations":{"key":"translations"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","wiki_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","articles":[{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"}]},{"translations":{"key":"translations"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","wiki_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","articles":[{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},{"name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"}]}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/articles/{id}/versions".format(id='id_example'),
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
    #    "/v1/articles/{id}".format(id='id_example'),
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
    #    "/v1/articles/versions/{id}".format(id='id_example'),
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
    #    "/v1/articles/{article_id}/versions/{version_id}".format(article_id='article_id_example', version_id='version_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_tags(client: TestClient):
    """Test case for unassign_tags

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_upload_image(client: TestClient):
    """Test case for upload_image

    Upload Image
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/upload-image",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

