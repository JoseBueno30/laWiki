# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.tag_list_v2 import TagListV2
from openapi_server.models.tag_v2 import TagV2


class BaseV3PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV3PublicApi.subclasses = BaseV3PublicApi.subclasses + (cls,)
    async def get_articles_tags_v3(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagListV2:
        """Retrieves all the tags from an article."""
        ...


    async def get_tag_v3(
        self,
        id: str,
    ) -> TagV2:
        """Get a tag by ID."""
        ...


    async def get_wiki_tags_v3(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagListV2:
        """Retrieve all the tags from a wiki."""
        ...
