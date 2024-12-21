# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401
from pydantic import StrictBool, StrictStr

from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2


class BaseInternalV3Api:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalV3Api.subclasses = BaseInternalV3Api.subclasses + (cls,)
    async def assign_wiki_tags_v3(
        self,
        id: str,
        user_email: StrictStr,
        admin: StrictBool,
        id_tags_body_v2: IdTagsBodyV2,
    ) -> None:
        """Assigns a list of tags, given their IDs, to a wiki"""
        ...


    async def check_wiki_by_idv3(
        self,
        id_name: str,
    ) -> None:
        """Check if a Wiki exits given its unique ID. """
        ...


    async def unassign_wiki_tags_v3(
        self,
        id: str,
        user_email: StrictStr,
        admin: StrictBool,
        ids: List[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to a Wiki."""
        ...


    async def update_rating_v3(
        self,
        user_email: StrictStr,
        admin: StrictBool,
        id: str,
        id_ratings_body: IdRatingsBody,
    ) -> None:
        """Update the rating of a Wiki give its unique ID and a rating"""
        ...
