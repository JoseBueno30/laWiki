# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.average_rating import AverageRating  # noqa: F401
from openapi_server.models.new_rating import NewRating  # noqa: F401
from openapi_server.models.rating import Rating  # noqa: F401


def test_delete_rating(client: TestClient):
    """Test case for delete_rating

    Delete Rating
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/ratings/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_ratings_articles_id(client: TestClient):
    """Test case for delete_ratings_articles_id

    Delete all ratings associated to an article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_edit_article_rating(client: TestClient):
    """Test case for edit_article_rating

    Edit Article's Rating
    """
    new_rating = {"author_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","value":0.8008281904610115}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/ratings/articles/{id}".format(id='id_example'),
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
    #    "/ratings/articles/{id}/average".format(id='id_example'),
    #    headers=headers,
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
    #    "/ratings/{id}".format(id='id_example'),
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
    #    "/ratings/articles/{articleId}/users/{userId}".format(articleId='article_id_example', userId='user_id_example'),
    #    headers=headers,
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
    #    "/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    json=new_rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

