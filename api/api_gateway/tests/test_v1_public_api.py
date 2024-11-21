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


def test_delete_comment(client: TestClient):
    """Test case for delete_comment

    Delete Comment
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/comments/{comment_id}".format(comment_id='comment_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_rating(client: TestClient):
    """Test case for delete_rating

    Delete Rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v1/ratings/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_edit_article_rating(client: TestClient):
    """Test case for edit_article_rating

    Edit Article's Rating
    """
    rating = {"article_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","creation_date":"2000-01-23","value":0.8008281904610115}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_average_rating(client: TestClient):
    """Test case for get_article_average_rating

    Get Article's average rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/ratings/articles/{id}/average".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


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
    #    "/v1/articles/author/{id}".format(id='id_example'),
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
    #    "/v1/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_by_name(client: TestClient):
    """Test case for get_article_by_name

    Get ArticleVersion by name
    """
    params = [("wiki", 'wiki_example'),     ("lan", 'en, es, fr')]
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


def test_get_article_comments(client: TestClient):
    """Test case for get_article_comments

    Get Articles Comments
    """
    params = [("order", 'recent'),     ("limit", 20),     ("offset", 0),     ("creation_date", '2013-10-20')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/comments/articles/{article_id}".format(article_id='article_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_from_specific_wiki(client: TestClient):
    """Test case for get_article_from_specific_wiki

    Get Article From Specific Wiki
    """
    params = [("lan", 'en, es, fr')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/wikis/{wiki_name}/articles/{article_name}".format(wiki_name='wiki_name_example', article_name='article_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_body_by_id(client: TestClient):
    """Test case for get_article_version_body_by_id

    Get ArticleVersion body
    """
    params = [("parsed", False),     ("lan", 'lan_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/versions/{id}/body".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_article_version_by_id(client: TestClient):
    """Test case for get_article_version_by_id

    Get ArticleVersion
    """
    params = [("lan", 'en, es, fr')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/articles/versions/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
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
    #    "/v1/articles/{id}/versions".format(id='id_example'),
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
    #    "/v1/articles/commented_by/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_articles_tags(client: TestClient):
    """Test case for get_articles_tags

    Get Articles Tag
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_rating(client: TestClient):
    """Test case for get_rating

    Get Rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/ratings/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_ratings_bu_user_on_article(client: TestClient):
    """Test case for get_ratings_bu_user_on_article

    Get rating made by an user in an article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/ratings/articles/{articleId}/users/{userId}".format(articleId='article_id_example', userId='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_tag(client: TestClient):
    """Test case for get_tag

    Get Tag
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_users_comments(client: TestClient):
    """Test case for get_users_comments

    Get Users Comments
    """
    params = [("article_id", 'article_id_example'),     ("order", 'recent'),     ("limit", 20),     ("offset", 0),     ("creation_date", '2013-10-20')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/comments/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki(client: TestClient):
    """Test case for get_wiki

    Get Wiki
    """
    params = [("lang", 'lang_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/wikis/{id_name}".format(id_name='id_name_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_wiki_tags(client: TestClient):
    """Test case for get_wiki_tags

    Get Wikis Tags
    """
    params = [("limit", 20),     ("offset", 0)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_comment(client: TestClient):
    """Test case for post_comment

    Post Comment
    """
    new_comment = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","body":"body"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/comments/articles/{article_id}".format(article_id='article_id_example'),
    #    headers=headers,
    #    json=new_comment,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_rate_article(client: TestClient):
    """Test case for rate_article

    Rate Article
    """
    new_rating = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","value":0.8008281904610115}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_articles(client: TestClient):
    """Test case for search_articles

    Search for Articles
    """
    params = [("wiki_id", 'wiki_id_example'),     ("name", 'name'),     ("tags", ['[\"tag1\",\"tag2\"]']),     ("offset", 0),     ("limit", 20),     ("order", 'none'),     ("creation_date", '2013-10-20'),     ("author_name", 'author_name_example'),     ("editor_name", 'editor_name_example'),     ("lan", 'en, es, fr')]
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


def test_search_wikis(client: TestClient):
    """Test case for search_wikis

    Search for Wikis
    """
    params = [("name", 'name_example'),     ("offset", 20),     ("limit", 0),     ("order", '2013-10-20'),     ("creation_date", '2024/01/01, 2023/01/01-2024/01/01'),     ("author_name", 'author_name'),     ("lang", 'lang_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/wikis",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

