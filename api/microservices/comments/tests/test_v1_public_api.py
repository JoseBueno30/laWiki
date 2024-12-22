# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.comment import Comment  # noqa: F401
from openapi_server.models.comment_list_response import CommentListResponse  # noqa: F401
from openapi_server.models.new_comment import NewComment  # noqa: F401


def test_v1_delete_comment(client: TestClient):
    """Test case for v1_delete_comment

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


def test_v1_get_articles_comments(client: TestClient):
    """Test case for v1_get_articles_comments

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


def test_v1_get_users_comments(client: TestClient):
    """Test case for v1_get_users_comments

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


def test_v1_post_comment(client: TestClient):
    """Test case for v1_post_comment

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

