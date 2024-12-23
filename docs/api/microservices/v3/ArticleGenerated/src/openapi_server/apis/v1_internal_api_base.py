# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.id_ratings_body_v1 import IdRatingsBodyV1
from openapi_server.models.id_tags_body_v1 import IdTagsBodyV1


class BaseV1InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1InternalApi.subclasses = BaseV1InternalApi.subclasses + (cls,)
    async def assign_article_tags_v1(
        self,
        id: StrictStr,
        id_tags_body_v1: Optional[IdTagsBodyV1],
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article"""
        ...


    async def check_article_by_idv1(
        self,
        id: StrictStr,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...


    async def unassign_article_tags_v1(
        self,
        id: StrictStr,
        ids: Annotated[List[StrictStr], Field(max_length=50, description="List of Tag IDs")],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def update_rating_v1(
        self,
        id: StrictStr,
        id_ratings_body_v1: Optional[IdRatingsBodyV1],
    ) -> None:
        """Update the rating of an Article give its unique ID and a rating"""
        ...
