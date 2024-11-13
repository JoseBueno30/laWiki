# coding: utf-8

from fastapi.testclient import TestClient




def test_delete_articles_comments(client: TestClient):
    """Test case for delete_articles_comments

    Delete Articles Comments
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/comments/articles/{article_id}".format(article_id='article_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

