# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.average_rating import AverageRating
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def delete_rating(
        self,
        id: str,
    ) -> None:
        """Delete the rating associated with the selected ID"""
        ...


    async def delete_ratings_articles_id(
        self,
        id: str,
    ) -> None:
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


    async def rate_article(
        self,
        id: str,
        new_rating: NewRating,
    ) -> Rating:
        """Create a rating for a given Article"""
        ...
