# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.new_tag import NewTag
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.tag import Tag
from openapi_server.models.wiki import Wiki
from openapi_server.security_api import get_token_oauth_token

class BaseV2AdminsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2AdminsApi.subclasses = BaseV2AdminsApi.subclasses + (cls,)
    async def create_wiki_v2(
        self,
        new_wiki: Optional[NewWiki],
    ) -> Wiki:
        """Create a new Wiki"""
        ...


    async def delete_tag_v2(
        self,
        id: StrictStr,
    ) -> None:
        """Delete a wiki tag."""
        ...


    async def post_wiki_tag_v2(
        self,
        id: Annotated[StrictStr, Field(description="The unique ID of the wiki.")],
        new_tag: Optional[NewTag],
    ) -> Tag:
        """Create a new tag in a given wiki."""
        ...


    async def remove_wiki_v2(
        self,
        id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")],
    ) -> None:
        """Remove Wiki with the matching ID."""
        ...


    async def update_wiki_v2(
        self,
        id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")],
        new_wiki: Optional[NewWiki],
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        ...