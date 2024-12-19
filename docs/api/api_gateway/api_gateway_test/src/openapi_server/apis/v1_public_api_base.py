# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article import Article
from openapi_server.models.article_list import ArticleList
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.article_version_body import ArticleVersionBody
from openapi_server.models.article_version_list import ArticleVersionList
from openapi_server.models.average_rating import AverageRating
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from openapi_server.models.new_comment import NewComment
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def delete_comment(
        self,
        comment_id: Annotated[StrictStr, Field(description="The unique ID of the article")],
    ) -> None:
        """Deletes an article&#39;s comment"""
        ...


    async def delete_rating(
        self,
        id: StrictStr,
    ) -> None:
        """Delete the rating associated with the selected ID"""
        ...


    async def edit_article_rating(
        self,
        id: StrictStr,
        new_rating: Optional[NewRating],
    ) -> Rating:
        """Update the value of an already existing Rating"""
        ...


    async def get_article_average_rating(
        self,
        id: StrictStr,
    ) -> AverageRating:
        """Get data about the average rating of the article"""
        ...


    async def get_article_by_author(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleList:
        """Get a list of Articles given an author&#39;s ID.  """
        ...


    async def get_article_by_id(
        self,
        id: StrictStr,
    ) -> Article:
        """Get an Article identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name(
        self,
        name: StrictStr,
        wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")],
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")],
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_comments(
        self,
        article_id: Annotated[StrictStr, Field(description="The unique ID of the article")],
        order: Annotated[Optional[StrictStr], Field(description="Set the order the comments will be shown. It is determined by date")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        creation_date: Annotated[Optional[date], Field(description="Single date or range")],
    ) -> CommentListResponse:
        """Retrieves all comments from an articles"""
        ...


    async def get_article_from_specific_wiki(
        self,
        wiki_name: Annotated[StrictStr, Field(description="Name of the wiki")],
        article_name: Annotated[StrictStr, Field(description="Name of the article")],
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")],
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the Wiki with the given name. Endpoint thought to access articles when only the names of the Wiki and Article are known, with a textual URL for example."""
        ...


    async def get_article_version_body_by_id(
        self,
        id: StrictStr,
        parsed: Annotated[Optional[StrictBool], Field(description="It indicates if the body must be parsed.")],
        lan: Annotated[Optional[StrictStr], Field(description="Language of the body, if parsed, original language if not specified")],
    ) -> ArticleVersionBody:
        ...


    async def get_article_version_by_id(
        self,
        id: StrictStr,
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")],
    ) -> ArticleVersion:
        """Get an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def get_article_version_list_by_article_id(
        self,
        id: StrictStr,
        offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleVersionList:
        """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
        ...


    async def get_articles_commented_by_user(
        self,
        id: StrictStr,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")],
        order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")],
    ) -> ArticleList:
        """Get a list of the Articles commented by a given user."""
        ...


    async def get_articles_tags(
        self,
        id: StrictStr,
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
    ) -> TagList:
        """Retrieves all the tags from an article."""
        ...


    async def get_rating(
        self,
        id: StrictStr,
    ) -> Rating:
        """Get the Rating with the provided ID"""
        ...


    async def get_ratings_bu_user_on_article(
        self,
        articleId: StrictStr,
        userId: StrictStr,
    ) -> Rating:
        ...


    async def get_tag(
        self,
        id: StrictStr,
    ) -> Tag:
        """Get a tag by ID. """
        ...


    async def get_users_comments(
        self,
        user_id: Annotated[StrictStr, Field(description="The unique ID of the user")],
        article_id: Annotated[Optional[StrictStr], Field(description="Fillters the results by the article's ID")],
        order: Annotated[Optional[StrictStr], Field(description="Set the order the comments will be shown. It is determined by date")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        creation_date: Annotated[Optional[date], Field(description="Single date or range")],
    ) -> CommentListResponse:
        """Retrieves all comments from an user"""
        ...


    async def get_wiki(
        self,
        id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")],
        lang: Annotated[Optional[StrictStr], Field(description="Language of the wiki to retrieve.")],
    ) -> Wiki:
        """Get Wiki with the matching ID."""
        ...


    async def get_wiki_tags(
        self,
        id: Annotated[StrictStr, Field(description="The unique ID of the wiki.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="Maximum amount of responses to be returned")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        ...


    async def post_comment(
        self,
        article_id: Annotated[StrictStr, Field(description="The unique ID of the article")],
        new_comment: Annotated[Optional[NewComment], Field(description="JSON object that contains the author and content of the comment")],
    ) -> Comment:
        """Posts a new comment in an article"""
        ...


    async def rate_article(
        self,
        id: StrictStr,
        new_rating: Optional[NewRating],
    ) -> Rating:
        """Create a rating for a given Article"""
        ...


    async def search_articles(
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
        lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, if none, the original language will be returned")],
    ) -> ArticleList:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...


    async def search_wikis(
        self,
        name: Annotated[Optional[StrictStr], Field(description="String to be searched within the wiki's name.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=1)]], Field(description="Maximum amount of results to be returned.")],
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")],
        order: Annotated[Optional[date], Field(description="Sorts the wikis by different criteria")],
        creation_date: Annotated[Optional[StrictStr], Field(description="Single date or range")],
        author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Wiki")],
        lang: Annotated[Optional[StrictStr], Field(description="Language of the wiki to retrieve.")],
    ) -> WikiList:
        """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
