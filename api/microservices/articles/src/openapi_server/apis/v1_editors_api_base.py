# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.models_v1.article_v1 import ArticleV1
from openapi_server.models.models_v1.article_version_v1 import ArticleVersionV1
from openapi_server.models.models_v1.new_article_v1 import NewArticleV1
from openapi_server.models.models_v1.new_article_version_v1 import NewArticleVersionV1


class BaseV1EditorsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1EditorsApi.subclasses = BaseV1EditorsApi.subclasses + (cls,)
    async def create_article_v1(
        self,
        new_article_v1: NewArticleV1,
    ) -> ArticleV1:
        """Create a new Article in a given wiki"""
        ...


    async def create_article_version_v1(
        self,
        id: str,
        new_article_version_v1: NewArticleVersionV1,
    ) -> ArticleVersionV1:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
        ...


    async def delete_article_by_idv1(
        self,
        id: str,
    ) -> None:
        """Delete an Article identified by it&#39;s unique ID"""
        ...


    async def delete_article_version_by_id_v1(
        self,
        id: str,
    ) -> None:
        """Delete an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def restore_article_version_v1(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        ...
