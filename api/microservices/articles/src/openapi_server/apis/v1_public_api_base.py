# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.models_v1.article_list_v1 import ArticleListV1
from openapi_server.models.models_v1.article_v1 import ArticleV1
from openapi_server.models.models_v1.article_version_list_v1 import ArticleVersionListV1
from openapi_server.models.models_v1.article_version_v1 import ArticleVersionV1


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def get_article_by_author_v1(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV1:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id_v1(
        self,
        id: str,
    ) -> ArticleV1:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name_v1(
        self,
        name: str,
        wiki: str,
    ) -> ArticleVersionV1:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_version_by_id_v1(
        self,
        id: str,
    ) -> ArticleVersionV1:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_idv1(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionListV1:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        ...


    async def get_articles_commented_by_user_v1(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV1:
        """Get a list of the Articles commented by a given user."""
        ...


    async def search_articles_v1(
        self,
        wiki_id: str,
        name: str,
        tags: list[str],
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        editor_name: str,
    ) -> ArticleListV1:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
