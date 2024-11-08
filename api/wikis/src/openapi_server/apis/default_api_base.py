# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def create_wiki(
        self,
        name: str,
        limit: int,
        offset: int,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Create a new Wiki"""
        ...


    async def get_one_wiki_by_name(
        self,
        name: str,
    ) -> Wiki:
        """Get the Wiki with the given name."""
        ...


    async def get_wiki(
        self,
        id: str,
    ) -> Wiki:
        """Get Wiki with the matching ID."""
        ...


    async def remove_wiki(
        self,
        id: str,
    ) -> None:
        """Remove Wiki with the matching ID."""
        ...


    async def search_wikis(
        self,
        name: str,
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
    ) -> WikiList:
        """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        ...


    async def update_wiki(
        self,
        id: str,
        new_wiki: NewWiki,
    ) -> Wiki:
        """Update Wiki with wiki the matching ID"""
        ...