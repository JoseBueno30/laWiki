# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401
from pydantic import StrictStr, StrictBool

from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.wiki_list_v2 import WikiListV2
from openapi_server.models.wiki_v2 import WikiV2


class BaseDefaultV3Api:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultV3Api.subclasses = BaseDefaultV3Api.subclasses + (cls,)
    async def create_wiki_v3(
        self,
        user_id: StrictStr,
        admin: StrictBool,
        new_wiki_v2: NewWikiV2,
    ) -> WikiV2:
        """Create a new Wiki"""
        ...


    async def get_wiki_v3(
        self,
        id_name: str,
        lang: str,
    ) -> WikiV2:
        """Get Wiki with the matching ID."""
        ...


    async def search_wikis_v3(
        self,
        name: str,
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        lang: str,
    ) -> WikiListV2:
        """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...
