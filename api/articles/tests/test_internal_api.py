# coding: utf-8

from fastapi.testclient import TestClient




def test_check_article_by_id(client: TestClient):
    """Test case for check_article_by_id

    Check Article
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "HEAD",
    #    "/articles/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

