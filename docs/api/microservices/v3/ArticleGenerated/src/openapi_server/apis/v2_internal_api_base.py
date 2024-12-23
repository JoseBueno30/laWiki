# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2


class BaseV2InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2InternalApi.subclasses = BaseV2InternalApi.subclasses + (cls,)
    async def assign_article_tags_v2(
        self,
        id: StrictStr,
        id_tags_body_v2: Optional[IdTagsBodyV2],
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article"""
        ...


    async def check_article_by_idv2(
        self,
        id: StrictStr,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...


    async def delete_articles_from_wiki_v2(
        self,
        id: StrictStr,
    ) -> None:
        ...


    async def unassign_article_tags_v2(
        self,
        id: StrictStr,
        ids: Annotated[List[StrictStr], Field(max_length=50, description="List of Tag IDs")],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def update_rating_v2(
        self,
        id: StrictStr,
        id_ratings_body_v2: Optional[IdRatingsBodyV2],
    ) -> None:
        """Update the rating of an Article give its unique ID and a rating"""
        ...
