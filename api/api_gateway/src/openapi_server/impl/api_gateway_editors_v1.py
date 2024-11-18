import json

from fastapi.exceptions import HTTPException
from typing import List

from fastapi import UploadFile
from fastapi.openapi.utils import status_code_ranges

from openapi_server.apis.v1_editors_api_base import BaseV1EditorsApi
from openapi_server.impl.utils import ARTICLES_URL,COMMENTS_URL,RATINGS_URL,TAGS_URL,WIKIS_URL
from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion
from openapi_server.models.tag_id_list import TagIDList

from dotenv import load_dotenv
import os

from openapi_server.impl.utils import forward_request

dotenv_path = os.path.abspath(os.path.join(__file__, "../../../../config.env"))
load_dotenv(dotenv_path=dotenv_path)
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

class APIGatewayEditorsV1(BaseV1EditorsApi):

    async def assign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        return await forward_request(method="PUT", url=f"{TAGS_URL}/v2/tags/articles/{id}", json=tag_id_list.to_dict())

    async def create_article(
        self,
        new_article: NewArticle,
    ) -> Article:
        """Create a new Article in a given wiki"""
        return await forward_request(method="POST", url=f"{ARTICLES_URL}/v2/articles", json=new_article.to_dict())


    async def create_article_version(
        self,
        id: str,
        new_article_version: NewArticleVersion,
    ) -> ArticleVersion:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
        return await forward_request(method="POST", url=f"{ARTICLES_URL}/v2/articles/{id}/versions", json=new_article_version.to_dict())


    async def delete_article_by_id(
        self,
        id: str,
    ) -> None:
        """Delete an Article identified by it&#39;s unique ID"""
        return await forward_request(method="DELETE", url=f"{ARTICLES_URL}/v2/articles/{id}")


    async def delete_article_version_by_id(
        self,
        id: str,
    ) -> None:
        """Delete an ArticleVersion identified by it&#39;s unique ID"""
        return await forward_request(method="DELETE", url=f"{ARTICLES_URL}/v2/articles/versions/{id}")


    async def restore_article_version(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        return await forward_request(method="PUT", url=f"{ARTICLES_URL}/v2/articles/{article_id}/versions/{version_id}")


    async def unassign_tags(
        self,
        id: str,
        ids: List[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        query_params = {"ids":ids}
        return await forward_request(method="DELETE", url=f"{TAGS_URL}/v2/tags/articles/{id}", query_params=query_params)


    async def upload_image(
        self,
        file: UploadFile,
    ) -> InlineResponse200:
        """Uploads an image file and returns the URL."""
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

