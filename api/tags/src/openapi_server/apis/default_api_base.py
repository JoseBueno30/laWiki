# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_list import TagList


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def assign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        ...


    async def delete_tag(
        self,
        id: str,
    ) -> None:
        """Delete a wiki tag."""
        ...


    async def get_articles_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> List[Tag]:
        """Retrieves all the tags from an article."""
        ...


    async def get_tag(
        self,
        id: str,
    ) -> Tag:
        """Get a tag by ID. """
        ...


    async def get_wiki_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        ...


    async def post_wiki_tag(
        self,
        id: str,
        new_tag: NewTag,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        ...


    async def unassign_tags(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...
