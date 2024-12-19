# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Any, List, Optional, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.article import Article  # noqa: F401
from openapi_server.models.article_version import ArticleVersion  # noqa: F401
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: F401
from openapi_server.models.new_article import NewArticle  # noqa: F401
from openapi_server.models.new_article_version import NewArticleVersion  # noqa: F401
from openapi_server.models.tag_id_list import TagIDList  # noqa: F401


def test_assign_tags_v2(client: TestClient):
    """Test case for assign_tags_v2

    Assign Tags
    """
    tag_id_list = {"tag_ids":["046b6c7f-0b8a-43b9-b35d-6489e6daee91","046b6c7f-0b8a-43b9-b35d-6489e6daee91"]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=tag_id_list,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_v2(client: TestClient):
    """Test case for create_article_v2

    Create Article
    """
    new_article = {"trasnlate_title":1,"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","title":"title","body":"body","wiki_id":"wiki_id","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}}]}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/articles",
    #    headers=headers,
    #    json=new_article,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_article_version_v2(client: TestClient):
    """Test case for create_article_version_v2

    Create ArticleVersion for an Article
    """
    new_article_version = {"author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"lan":"lan","translate_title":1,"title":"title","body":"body","tags":[{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}},{"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","tag":{"key":"tag"}}]}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/articles/{id}/versions".format(id='id_example'),
    #    headers=headers,
    #    json=new_article_version,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_article_by_idv2(client: TestClient):
    """Test case for delete_article_by_idv2

    Delete Article
    """

    headers = {
        "Authorization": "Bearer special-key",
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
        "Authorization": "Bearer special-key",
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
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/articles/{article_id}/versions/{version_id}".format(article_id='article_id_example', version_id='version_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_unassign_tags_v2(client: TestClient):
    """Test case for unassign_tags_v2

    Unassign Tags
    """
    params = [("ids", ['[\"tag1\",\"tag2\"]'])]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_upload_image_v2(client: TestClient):
    """Test case for upload_image_v2

    Upload Image
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/upload-image",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

