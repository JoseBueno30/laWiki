# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki


class BaseAdminsApiV2:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAdminsApiV2.subclasses = BaseAdminsApiV2.subclasses + (cls,)
    async def create_wiki(
        self,
        name: str,
        limit: int,
        offset: int,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Create a new Wiki"""
        ...


    async def remove_wiki(
        self,
        id: str,
    ) -> None:
        """Remove Wiki with the matching ID."""
        ...


    async def update_wiki(
        self,
        id: str,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        ...
