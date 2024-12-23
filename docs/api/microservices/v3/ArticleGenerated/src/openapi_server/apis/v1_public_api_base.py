# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article_list_v1 import ArticleListV1
from openapi_server.models.article_v1 import ArticleV1
from openapi_server.models.article_version_list_v1 import ArticleVersionListV1
from openapi_server.models.article_version_v1 import ArticleVersionV1


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def get_article_by_author_v1(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleListV1:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id_v1(
        self,
        id: StrictStr,
    ) -> ArticleV1:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name_v1(
        self,
        name: StrictStr,
        wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")],
    ) -> ArticleVersionV1:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_version_by_id_v1(
        self,
        id: StrictStr,
    ) -> ArticleVersionV1:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_idv1(
        self,
        id: StrictStr,
        offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleVersionListV1:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date and support pagination."""
        ...


    async def get_articles_commented_by_user_v1(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleListV1:
        """Get a list of the Articles commented by a given user."""
        ...


    async def search_articles_v1(
        self,
        wiki_id: Annotated[Optional[StrictStr], Field(description="The ID of the wiki where the serch will be made")],
        name: Annotated[Optional[StrictStr], Field(description="Search query for the name of the article")],
        tags: Annotated[Optional[List[StrictStr]], Field(description="A comma-separated list of tag IDs to search for")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
        creation_date: Annotated[Optional[date], Field(description="Single date or range")],
        author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Article")],
        editor_name: Annotated[Optional[StrictStr], Field(description="Filter for the editors of the Article")],
    ) -> ArticleListV1:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
