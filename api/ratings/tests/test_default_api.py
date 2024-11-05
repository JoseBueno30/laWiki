# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.inline_response200 import InlineResponse200  # noqa: F401
from openapi_server.models.new_rating import NewRating  # noqa: F401
from openapi_server.models.rating import Rating  # noqa: F401
from openapi_server.models.rating_list import RatingList  # noqa: F401


def test_delete_ratings_id(client: TestClient):
    """Test case for delete_ratings_id

    Delete rating by ID
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


def test_get_ratings_article_id(client: TestClient):
    """Test case for get_ratings_article_id

    Get all ratings of an article
    """
    params = [("order", 'order_example'),     ("limit", 56),     ("offset", 56)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ratings/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_ratings_article_id_average(client: TestClient):
    """Test case for get_ratings_article_id_average

    Get average rating on selected Article
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


def test_get_ratings_id(client: TestClient):
    """Test case for get_ratings_id

    Get rating by ID
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


def test_get_ratings_user_id(client: TestClient):
    """Test case for get_ratings_user_id

    Get the rating from an user
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ratings/users/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_ratings_article_id(client: TestClient):
    """Test case for post_ratings_article_id

    Create rating on article
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


def test_put_ratings_article_id(client: TestClient):
    """Test case for put_ratings_article_id

    Edit rating of an article
    """
    rating = {"article_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","author":{"image":"https://openapi-generator.tech","name":"name","id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"},"id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","creation_date":"2000-01-23","value":0.8008281904610115}

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

