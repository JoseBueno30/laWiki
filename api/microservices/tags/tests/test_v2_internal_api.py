# coding: utf-8

from fastapi.testclient import TestClient




def test_delete_wiki_tags_v2(client: TestClient):
    """Test case for delete_wiki_tags_v2

    Delete Wiki Tags
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/v2/tags/wikis/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

