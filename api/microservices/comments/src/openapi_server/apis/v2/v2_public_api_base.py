# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from openapi_server.models.new_comment import NewComment


class BaseV2PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2PublicApi.subclasses = BaseV2PublicApi.subclasses + (cls,)
    async def v2_delete_comment(
        self,
        comment_id: str,
        user_id: str,
        admin: bool,
    ) -> None:
        """Deletes an article&#39;s comment"""
        ...


    async def v2_get_articles_comments(
        self,
        article_id: str,
        order: str,
        limit: int,
        offset: int,
        creation_date: str,
    ) -> CommentListResponse:
        """Retrieves all comments from an article"""
        ...


    async def v2_get_users_comments(
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


    async def v2_post_comment(
        self,
        article_id: str,
        user_id: str,
        admin: bool,
        new_comment: NewComment,
    ) -> Comment:
        """Posts a new comment in an article"""
        ...
