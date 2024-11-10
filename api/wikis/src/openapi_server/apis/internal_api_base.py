# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body import IdTagsBody


class BaseInternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalApi.subclasses = BaseInternalApi.subclasses + (cls,)
    async def assign_wiki_tags(
        self,
        id: str,
        id_tags_body: IdTagsBody,
    ) -> None:
        """Assigns a list of tags, given their IDs, to a wiki"""
        ...


    async def check_wiki_by_id(
        self,
        id: str,
    ) -> None:
        """Check if a Wiki exits given its unique ID. """
        ...


    async def unassign_article_tags(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to a Wiki."""
        ...


    async def update_rating(
        self,
        id: str,
        id_ratings_body: IdRatingsBody,
    ) -> None:
        """Update the rating of a Wiki give its unique ID and a rating"""
        ...
