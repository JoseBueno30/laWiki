# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag


class BaseAdminsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAdminsApi.subclasses = BaseAdminsApi.subclasses + (cls,)
    async def delete_tag(
        self,
        id: str,
    ) -> None:
        """Delete a wiki tag."""
        ...


    async def post_wiki_tag(
        self,
        id: str,
        new_tag: NewTag,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        ...
