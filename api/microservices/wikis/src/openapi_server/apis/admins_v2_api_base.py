# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.wiki_v2 import WikiV2


class BaseAdminsV2Api:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAdminsV2Api.subclasses = BaseAdminsV2Api.subclasses + (cls,)
    async def remove_wiki_v2(
        self,
        id_name: str,
    ) -> None:
        """Remove Wiki with the matching ID."""
        ...


    async def update_wiki_v2(
        self,
        id_name: str,
        new_wiki_v2: NewWikiV2,
    ) -> WikiV2:
        """Update Wiki with wiki the matching ID"""
        ...
