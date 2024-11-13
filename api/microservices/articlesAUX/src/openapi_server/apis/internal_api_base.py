# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body import IdTagsBody


class BaseInternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalApi.subclasses = BaseInternalApi.subclasses + (cls,)
    async def assign_article_tags(
        self,
        id: str,
        id_tags_body: IdTagsBody,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article"""
        ...


    async def check_article_by_id(
        self,
        id: str,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...


    async def unassign_article_tags(
        self,
        id: str,
        ids: List[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def update_rating(
        self,
        id: str,
        id_ratings_body: IdRatingsBody,
    ) -> None:
        """Update the rating of an Article give its unique ID and a rating"""
        ...
