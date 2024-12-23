# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBool, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2


class BaseV3InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV3InternalApi.subclasses = BaseV3InternalApi.subclasses + (cls,)
    async def assign_article_tags_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        id_tags_body_v2: Optional[IdTagsBodyV2],
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article"""
        ...


    async def check_article_by_idv3(
        self,
        id: StrictStr,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...


    async def delete_articles_from_wiki_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        ...


    async def unassign_article_tags_v3(
        self,
        id: StrictStr,
        ids: Annotated[List[StrictStr], Field(max_length=50, description="List of Tag IDs")],
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...


    async def update_rating_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        id_ratings_body_v2: Optional[IdRatingsBodyV2],
    ) -> None:
        """Update the rating of an Article give its unique ID and a rating"""
        ...
