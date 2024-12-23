import json

from fastapi.exceptions import HTTPException
from typing import List

from fastapi import UploadFile

from openapi_server.apis.v2_apis.v2_editors_api_base import BaseV2EditorsApi
from openapi_server.impl.utils import ARTICLES_API_URL, TAGS_API_URL
from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.extra_models import TokenModel
from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion
from openapi_server.models.tag_id_list import TagIDList

from dotenv import load_dotenv
import os

from openapi_server.impl.utils import forward_request

dotenv_path = os.path.abspath(os.path.join(__file__, "../../../../../config.env"))
load_dotenv(dotenv_path=dotenv_path)
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")


class APIGatewayEditorsV2(BaseV2EditorsApi):

    def __init__(self):
        super().__init__()

    async def assign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
        decoded_token: TokenModel,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="PUT", url=f"{TAGS_API_URL}/v3/tags/articles/{id}", json=tag_id_list.to_dict(), headers_params=headers_params)

    async def create_article(
        self,
        new_article: NewArticle,
        decoded_token: TokenModel,
    ) -> Article:
        """Create a new Article in a given wiki"""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="POST", url=f"{ARTICLES_API_URL}/v3/articles", json=new_article.to_dict(), headers_params=headers_params)


    async def create_article_version(
        self,
        id: str,
        new_article_version: NewArticleVersion,
        decoded_token: TokenModel,
    ) -> ArticleVersion:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="POST", url=f"{ARTICLES_API_URL}/v3/articles/{id}/versions", json=new_article_version.to_dict(), headers_params=headers_params)


    async def delete_article_by_id(
        self,
        id: str,
        decoded_token: TokenModel,
    ) -> None:
        """Delete an Article identified by it&#39;s unique ID"""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="DELETE", url=f"{ARTICLES_API_URL}/v3/articles/{id}", headers_params=headers_params)


    async def delete_article_version_by_id(
        self,
        id: str,
        decoded_token: TokenModel,
    ) -> None:
        """Delete an ArticleVersion identified by it&#39;s unique ID"""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="DELETE", url=f"{ARTICLES_API_URL}/v3/articles/versions/{id}", headers_params=headers_params)


    async def restore_article_version(
        self,
        article_id: str,
        version_id: str,
        decoded_token: TokenModel,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        return await forward_request(method="PUT", url=f"{ARTICLES_API_URL}/v3/articles/{article_id}/versions/{version_id}", headers_params=headers_params)


    async def unassign_tags(
        self,
        id: str,
        ids: List[str],
        decoded_token: TokenModel,
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        headers_params = {
            "user-id": decoded_token.user_info["id"],
            "admin": decoded_token.user_info["admin"]
        }
        query_params = {"ids":ids}
        return await forward_request(method="DELETE", url=f"{TAGS_API_URL}/v3/tags/articles/{id}", query_params=query_params, headers_params=headers_params)


    async def upload_image(
        self,
        file: UploadFile,
    ) -> InlineResponse200:
        """Uploads an image file and returns the URL."""
        print("---------------")
        print(DROPBOX_ACCESS_TOKEN)
        print("---------------")
        print(file.filename)

        file_name = file.filename
        content_type = file.content_type

        if not content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Bad Request, invalid file format")

        upload_headers_params = {
            "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
            "Dropbox-API-Arg": json.dumps({"autorename":True, "path":f"/{file_name}", "mode":"add", "mute":True, "strict_conflict":True}),
            "Content-Type": "application/octet-stream"
        }
        content = await file.read()

        response = await forward_request(method = "POST", url = "https://content.dropboxapi.com/2/files/upload", headers_params=upload_headers_params, content=content)

        link_headers_params = {
            "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        request_body= {
            "path": response["path_lower"],
            "settings":{
                "access": "viewer",
                "allow_download": True,
                "audience": "public"
            }
        }

        link_response = await forward_request(method="POST", url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings", headers_params=link_headers_params, json=request_body)

        url = link_response["url"]

        return InlineResponse200(url=url.replace("dl=0", "raw=1"))

