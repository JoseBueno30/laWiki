# coding: utf-8

from fastapi.testclient import TestClient


from datetime import date  # noqa: F401
from pydantic import Field, StrictBool, StrictInt, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.article import Article  # noqa: F401
from openapi_server.models.article_list import ArticleList  # noqa: F401
from openapi_server.models.article_version import ArticleVersion  # noqa: F401
from openapi_server.models.article_version_body import ArticleVersionBody  # noqa: F401
from openapi_server.models.article_version_list import ArticleVersionList  # noqa: F401
from openapi_server.models.average_rating import AverageRating  # noqa: F401
from openapi_server.models.comment import Comment  # noqa: F401
from openapi_server.models.comment_list_response import CommentListResponse  # noqa: F401
from openapi_server.models.new_comment import NewComment  # noqa: F401
from openapi_server.models.new_rating import NewRating  # noqa: F401
from openapi_server.models.rating import Rating  # noqa: F401
from openapi_server.models.tag import Tag  # noqa: F401
from openapi_server.models.tag_list import TagList  # noqa: F401
from openapi_server.models.wiki import Wiki  # noqa: F401
from openapi_server.models.wiki_list import WikiList  # noqa: F401


def test_delete_comment_v2(client: TestClient):
    """Test case for delete_comment_v2

    Delete Comment
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/comments/{comment_id}".format(comment_id='comment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_rating_v2(client: TestClient):
    """Test case for delete_rating_v2

    Delete Rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/ratings/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_edit_article_rating_v2(client: TestClient):
    """Test case for edit_article_rating_v2

    Edit Article's Rating
    """
    new_rating = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","value":0.8008281904610115}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v2/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_average_rating_v2(client: TestClient):
    """Test case for get_article_average_rating_v2

    Get Article's average rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/ratings/articles/{id}/average".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_author_v2(client: TestClient):
    """Test case for get_article_by_author_v2

    Get Articles by Author
    """
    params = [("offset", 0),     ("limit", 0),     ("order", 'recent, oldest')]
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
    params = [("wiki", 'wiki_example'),     ("lan", 'en, es, fr')]
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


def test_get_article_comments_v2(client: TestClient):
    """Test case for get_article_comments_v2

    Get Articles Comments
    """
    params = [("order", 'recent'),     ("limit", 20),     ("offset", 0),     ("creation_date", '2013-10-20')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/comments/articles/{article_id}".format(article_id='article_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_from_specific_wiki_v2(client: TestClient):
    """Test case for get_article_from_specific_wiki_v2

    Get Article From Specific Wiki
    """
    params = [("lan", 'en, es, fr')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/wikis/{wiki_name}/articles/{article_name}".format(wiki_name='wiki_name_example', article_name='article_name_example'),
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
    params = [("lan", 'en, es, fr')]
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


def test_get_articles_tags_v2(client: TestClient):
    """Test case for get_articles_tags_v2

    Get Articles Tag
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_rating_v2(client: TestClient):
    """Test case for get_rating_v2

    Get Rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/ratings/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_ratings_bu_user_on_article_v2(client: TestClient):
    """Test case for get_ratings_bu_user_on_article_v2

    Get rating made by an user in an article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/ratings/articles/{articleId}/users/{userId}".format(articleId='article_id_example', userId='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_tag_v2(client: TestClient):
    """Test case for get_tag_v2

    Get Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_users_comments_v2(client: TestClient):
    """Test case for get_users_comments_v2

    Get Users Comments
    """
    params = [("article_id", 'article_id_example'),     ("order", 'recent'),     ("limit", 20),     ("offset", 0),     ("creation_date", '2013-10-20')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/comments/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_tags_v2(client: TestClient):
    """Test case for get_wiki_tags_v2

    Get Wikis Tags
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_v2(client: TestClient):
    """Test case for get_wiki_v2

    Get Wiki
    """
    params = [("lang", 'lang_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_comment_v2(client: TestClient):
    """Test case for post_comment_v2

    Post Comment
    """
    new_comment = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","body":"body"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/comments/articles/{article_id}".format(article_id='article_id_example'),
    #    headers=headers,
    #    json=new_comment,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_rate_article_v2(client: TestClient):
    """Test case for rate_article_v2

    Rate Article
    """
    new_rating = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","value":0.8008281904610115}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v2/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_articles_v2(client: TestClient):
    """Test case for search_articles_v2

    Search for Articles
    """
    params = [("wiki_id", 'wiki_id_example'),     ("name", 'name'),     ("tags", ['[\"tag1\",\"tag2\"]']),     ("offset", 0),     ("limit", 20),     ("order", 'none'),     ("creation_date", '2013-10-20'),     ("author_name", 'author_name_example'),     ("editor_name", 'editor_name_example'),     ("lan", 'en, es, fr')]
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


def test_search_wikis_v2(client: TestClient):
    """Test case for search_wikis_v2

    Search for Wikis
    """
    params = [("name", 'name_example'),     ("limit", 20),     ("offset", 0),     ("order", '2013-10-20'),     ("creation_date", '2024/01/01, 2023/01/01-2024/01/01'),     ("author_name", 'author_name'),     ("lang", 'lang_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v2/wikis",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

