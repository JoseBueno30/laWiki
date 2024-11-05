# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.new_article_version import NewArticleVersion


class BaseEditorsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseEditorsApi.subclasses = BaseEditorsApi.subclasses + (cls,)
    async def create_article_version(
        self,
        id: str,
        new_article_version: NewArticleVersion,
    ) -> ArticleVersion:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article. If not given an Article, a new one is created."""
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
