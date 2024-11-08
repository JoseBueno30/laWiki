# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.article import Article
from openapi_server.models.article_list import ArticleList
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.article_version_list import ArticleVersionList


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def get_article_by_author(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleList:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id(
        self,
        id: str,
    ) -> Article:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name(
        self,
        name: str,
        wiki: str,
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_version_by_id(
        self,
        id: str,
    ) -> ArticleVersion:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_id(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionList:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        ...


    async def get_articles_commented_by_user(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleList:
        """Get a list of the Articles commented by a given user."""
        ...


    async def search_articles(
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
    ) -> ArticleList:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
