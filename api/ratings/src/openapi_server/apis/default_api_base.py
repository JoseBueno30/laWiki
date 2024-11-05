# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from openapi_server.models.rating_list import RatingList


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def delete_ratings_id(
        self,
        id: str,
    ) -> None:
        """Delete the rating associated with the selected ID"""
        ...


    async def get_ratings_article_id(
        self,
        id: str,
        order: str,
        limit: int,
        offset: int,
    ) -> RatingList:
        ...


    async def get_ratings_article_id_average(
        self,
        id: str,
    ) -> InlineResponse200:
        ...


    async def get_ratings_id(
        self,
        id: str,
    ) -> Rating:
        ...


    async def get_ratings_user_id(
        self,
        id: str,
    ) -> float:
        ...


    async def post_ratings_article_id(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        ...


    async def put_ratings_article_id(
        self,
        id: str,
        rating: Rating,
    ) -> Rating:
        """This endpoint must do the same as Post but editting the value instead of creating a new one"""
        ...
