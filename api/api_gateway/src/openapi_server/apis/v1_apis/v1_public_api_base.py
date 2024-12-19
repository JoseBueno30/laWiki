# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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
        comment_id: str,
    ) -> None:
        """Deletes an article&#39;s comment"""
        ...


    async def delete_rating(
        self,
        id: str,
    ) -> None:
        """Delete the rating associated with the selected ID"""
        ...


    async def edit_article_rating(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        """Update the value of an already existing Rating"""
        ...


    async def get_article_average_rating(
        self,
        id: str,
    ) -> AverageRating:
        """Get data about the average rating of the article"""
        ...


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
        """Get an Article identified by it&#39;s unique ID"""
        ...


    async def get_article_by_name(
        self,
        name: str,
        wiki: str,
        lan: str,
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
        ...


    async def get_article_comments(
        self,
        article_id: str,
        order: str,
        limit: int,
        offset: int,
        creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an articles"""
        ...


    async def get_article_from_specific_wiki(
        self,
        wiki_name: str,
        article_name: str,
        lan: str,
    ) -> ArticleVersion:
        """Get the most recent ArticleVersion the Article with the given name from the Wiki with the given name. Endpoint thought to access articles when only the names of the Wiki and Article are known, with a textual URL for example."""
        ...


    async def get_article_version_body_by_id(
        self,
        id: str,
        parsed: bool,
        lan: str,
    ) -> ArticleVersionBody:
        ...


    async def get_article_version_by_id(
        self,
        id: str,
        lan: str,
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


    async def get_articles_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieves all the tags from an article."""
        ...


    async def get_rating(
        self,
        id: str,
    ) -> Rating:
        """Get the Rating with the provided ID"""
        ...


    async def get_ratings_bu_user_on_article(
        self,
        articleId: str,
        userId: str,
    ) -> Rating:
        ...


    async def get_tag(
        self,
        id: str,
    ) -> Tag:
        """Get a tag by ID. """
        ...


    async def get_users_comments(
        self,
        user_id: str,
        article_id: str,
        order: str,
        limit: int,
        offset: int,
        creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an user"""
        ...


    async def get_wiki(
        self,
        id_name: str,
        lang: str,
    ) -> Wiki:
        """Get Wiki with the matching ID."""
        ...


    async def get_wiki_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        ...


    async def post_comment(
        self,
        article_id: str,
        new_comment: NewComment,
    ) -> Comment:
        """Posts a new comment in an article"""
        ...


    async def rate_article(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        """Create a rating for a given Article"""
        ...


    async def search_articles(
        self,
        wiki_id: str,
        name: str,
        tags: List[str],
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        editor_name: str,
        lan: str,
    ) -> ArticleList:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...


    async def search_wikis(
        self,
        name: str,
        limit: int,
        offset: int,
        order: str,
        creation_date: str,
        author_name: str,
        lang: str,
    ) -> WikiList:
        """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
