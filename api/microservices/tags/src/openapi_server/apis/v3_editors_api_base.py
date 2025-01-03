# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_tag_v2 import NewTagV2
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_v2 import TagV2


class BaseV3EditorsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV3EditorsApi.subclasses = BaseV3EditorsApi.subclasses + (cls,)
    async def assign_tags_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        ...


    async def delete_tag_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
    ) -> None:
        """Delete a wiki tag."""
        ...


    async def post_wiki_tag_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
        new_tag_v2: NewTagV2,
    ) -> TagV2:
        """Create a new tag in a given wiki."""
        ...


    async def unassign_tags_v3(
        self,
        id: str,
        ids: List[str],
        user_id: str,
        admin: str,
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        ...
