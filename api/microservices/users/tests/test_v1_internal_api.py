# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.user_info import UserInfo  # noqa: F401
from openapi_server.models.verify_response import VerifyResponse  # noqa: F401


def test_put_user_rating(client: TestClient):
    """Test case for put_user_rating

    Update user rating
    """
    body = 3.4

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/users/{user_id}/rating".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_verify_token(client: TestClient):
    """Test case for put_verify_token

    Verify user token
    """
    body = 'body_example'

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/v1/verify_token",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

