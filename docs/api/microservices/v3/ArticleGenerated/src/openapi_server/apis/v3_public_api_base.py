# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article_list_v2 import ArticleListV2
from openapi_server.models.article_v2 import ArticleV2
from openapi_server.models.article_version_list_v2 import ArticleVersionListV2
from openapi_server.models.article_version_v2 import ArticleVersionV2
from openapi_server.models.inline_response200_v2 import InlineResponse200V2


class BaseV3PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV3PublicApi.subclasses = BaseV3PublicApi.subclasses + (cls,)
    async def get_article_by_author_v3(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleListV2:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id_v3(
        self,
        id: StrictStr,
    ) -> ArticleV2:
        """Get an Article identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name_v3(
        self,
        name: StrictStr,
        wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")],
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, any language if not specified")],
    ) -> ArticleVersionV2:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_version_body_by_idv3(
        self,
        id: StrictStr,
        parsed: Annotated[Optional[StrictBool], Field(description="It indicates if the body must be parsed.")],
        lan: Annotated[Optional[StrictStr], Field(description="Language of the body, if parsed, original language if not specified")],
    ) -> InlineResponse200V2:
        ...


    async def get_article_version_by_id_v3(
        self,
        id: StrictStr,
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, original language if not specified")],
    ) -> ArticleVersionV2:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_idv3(
        self,
        id: StrictStr,
        offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleVersionListV2:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        ...


    async def get_articles_commented_by_user_v3(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleListV2:
        """Get a list of the Articles commented by a given user."""
        ...


    async def search_articles_v3(
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
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, original language if not specified")],
    ) -> ArticleListV2:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
