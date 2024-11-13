# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.article_list_v2 import ArticleListV2
from openapi_server.models.article_v2 import ArticleV2
from openapi_server.models.article_version_list_v2 import ArticleVersionListV2
from openapi_server.models.article_version_v2 import ArticleVersionV2
from openapi_server.models.inline_response200_v2 import InlineResponse200V2


class BaseV2PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2PublicApi.subclasses = BaseV2PublicApi.subclasses + (cls,)
    async def get_article_by_author_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id_v2(
        self,
        id: str,
    ) -> ArticleV2:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name_v2(
        self,
        name: str,
        wiki: str,
    ) -> ArticleVersionV2:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_version_body_by_idv2(
        self,
        id: str,
        parsed: bool,
        lan: str,
    ) -> InlineResponse200V2:
        ...


    async def get_article_version_by_id_v2(
        self,
        id: str,
        lan: str,
    ) -> ArticleVersionV2:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_idv2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionListV2:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        ...


    async def get_articles_commented_by_user_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        """Get a list of the Articles commented by a given user."""
        ...


    async def search_articles_v2(
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
    ) -> ArticleListV2:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
