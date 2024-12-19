# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.new_tag import NewTag  # noqa: F401
from openapi_server.models.new_wiki import NewWiki  # noqa: F401
from openapi_server.models.tag import Tag  # noqa: F401
from openapi_server.models.wiki import Wiki  # noqa: F401


def test_create_wiki_v2(client: TestClient):
    """Test case for create_wiki_v2

    Create Wiki
    """
    new_wiki = {"image":"https://openapi-generator.tech","author":"author","name":"[{\"en\":\"Wiki name\",\"es\":\"Nombre de wiki\"}]","description":"description","lang":"lang","translate":1}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/wikis",
    #    headers=headers,
    #    json=new_wiki,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_tag_v2(client: TestClient):
    """Test case for delete_tag_v2

    Delete Tag
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_wiki_tag_v2(client: TestClient):
    """Test case for post_wiki_tag_v2

    Create Tag
    """
    new_tag = {"translation":1,"lan":"lan","tag":"tag"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_tag,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_remove_wiki_v2(client: TestClient):
    """Test case for remove_wiki_v2

    Remove Wiki
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_wiki_v2(client: TestClient):
    """Test case for update_wiki_v2

    Update Wiki
    """
    new_wiki = {"image":"https://openapi-generator.tech","author":"author","name":"[{\"en\":\"Wiki name\",\"es\":\"Nombre de wiki\"}]","description":"description","lang":"lang","translate":1}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #    json=new_wiki,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

