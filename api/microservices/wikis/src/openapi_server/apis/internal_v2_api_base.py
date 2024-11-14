# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2


class BaseInternalV2Api:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalV2Api.subclasses = BaseInternalV2Api.subclasses + (cls,)
    async def assign_wiki_tags_v2(
        self,
        id: str,
        id_tags_body_v2: IdTagsBodyV2,
    ) -> None:
        """Assigns a list of tags, given their IDs, to a wiki"""
        ...


    async def check_wiki_by_idv2(
        self,
        id_name: str,
    ) -> None:
        """Check if a Wiki exits given its unique ID. """
        ...


    async def unassign_wiki_tags_v2(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to a Wiki."""
        ...


    async def update_rating_v2(
        self,
        id: str,
        id_ratings_body: IdRatingsBody,
    ) -> None:
        """Update the rating of a Wiki give its unique ID and a rating"""
        ...
