# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion
from openapi_server.models.tag_id_list import TagIDList


class BaseV2EditorsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2EditorsApi.subclasses = BaseV2EditorsApi.subclasses + (cls,)
    async def assign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        ...


    async def create_article(
        self,
        new_article: NewArticle,
    ) -> Article:
        """Create a new Article in a given wiki"""
        ...


    async def create_article_version(
        self,
        id: str,
        new_article_version: NewArticleVersion,
    ) -> ArticleVersion:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
        ...


    async def delete_article_by_id(
        self,
        id: str,
    ) -> None:
        """Delete an Article identified by it&#39;s unique ID"""
        ...


    async def delete_article_version_by_id(
        self,
        id: str,
    ) -> None:
        """Delete an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def restore_article_version(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        ...


    async def unassign_tags(
        self,
        id: str,
        ids: List[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def upload_image(
        self,
        file: str,
    ) -> InlineResponse200:
        """Uploads an image file and returns the URL."""
        ...
