# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.extra_models import TokenModel
from openapi_server.models.new_tag import NewTag
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.tag import Tag
from openapi_server.models.wiki import Wiki


class BaseV2AdminsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2AdminsApi.subclasses = BaseV2AdminsApi.subclasses + (cls,)
    async def create_wiki(
        self,
        new_wiki: NewWiki,
        decoded_token: TokenModel,
    ) -> Wiki:
        """Create a new Wiki"""
        ...


    async def delete_tag(
        self,
        id: str,
        decoded_token: TokenModel,
    ) -> None:
        """Delete a wiki tag."""
        ...


    async def post_wiki_tag(
        self,
        id: str,
        new_tag: NewTag,
        decoded_token: TokenModel,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        ...


    async def remove_wiki(
        self,
        id_name: str,
        decoded_token: TokenModel,
    ) -> None:
        """Remove Wiki with the matching ID."""
        ...


    async def update_wiki(
        self,
        id_name: str,
        new_wiki: NewWiki,
        decoded_token: TokenModel,
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        ...
