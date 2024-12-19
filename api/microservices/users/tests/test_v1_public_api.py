# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.new_user_info import NewUserInfo  # noqa: F401
from openapi_server.models.user_info import UserInfo  # noqa: F401
from openapi_server.models.verify_response import VerifyResponse  # noqa: F401


def test_get_user_info(client: TestClient):
    """Test case for get_user_info

    Get user info
    """

    headers = {
        "user_email": 'user_email_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_verify_token(client: TestClient):
    """Test case for post_verify_token

    Verify user token
    """
    params = [("auth_token", 'auth_token_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/verify_token",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_users_user_email(client: TestClient):
    """Test case for put_users_user_email

    Update user info
    """
    new_user_info = {"image":"https://openapi-generator.tech","username":"username"}

    headers = {
        "user_email": 'user_email_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=new_user_info,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_users_user_id_image(client: TestClient):
    """Test case for put_users_user_id_image

    Update user image
    """
    body = 'body_example'

    headers = {
        "user_email": 'user_email_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/users/{user_id}/image".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_users_user_id_username(client: TestClient):
    """Test case for put_users_user_id_username

    Update user username
    """
    body = 'body_example'

    headers = {
        "user_email": 'user_email_example',
        "admin": True,
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/users/{user_id}/username".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

