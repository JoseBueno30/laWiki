# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def get_articles_tags_v1(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieves all the tags from an article."""
        ...


    async def get_tag_v1(
        self,
        id: str,
    ) -> Tag:
        """Get a tag by ID. """
        ...


    async def get_wiki_tags_v1(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        ...
