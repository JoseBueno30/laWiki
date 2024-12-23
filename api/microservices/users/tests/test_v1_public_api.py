# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.public_user_info import PublicUserInfo  # noqa: F401


def test_get_user_info(client: TestClient):
    """Test case for get_user_info

    Get user info
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/users/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

