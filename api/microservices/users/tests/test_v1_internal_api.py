# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_rating import NewRating  # noqa: F401


def test_head_users_user_email(client: TestClient):
    """Test case for head_users_user_email

    Check user
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/v1/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_v1_users_user_email_rating(client: TestClient):
    """Test case for put_v1_users_user_email_rating

    Update user rating
    """
    new_rating = {"rating":0.8008282}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/users/{user_id}/rating".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=new_rating,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

