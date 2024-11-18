# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.models_v1.id_ratings_body_v1 import IdRatingsBodyV1
from openapi_server.models.models_v1.id_tags_body_v1 import IdTagsBodyV1


class BaseV1InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1InternalApi.subclasses = BaseV1InternalApi.subclasses + (cls,)
    async def assign_article_tags_v1(
        self,
        id: str,
        id_tags_body_v1: IdTagsBodyV1,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article"""
        ...


    async def check_article_by_idv1(
        self,
        id: str,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...


    async def unassign_article_tags_v1(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def update_rating_v1(
        self,
        id: str,
        id_ratings_body_v1: IdRatingsBodyV1,
    ) -> None:
        """Update the rating of an Article give its unique ID and a rating"""
        ...
