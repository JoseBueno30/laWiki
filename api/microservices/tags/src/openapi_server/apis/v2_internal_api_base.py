# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401



class BaseV2InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV2InternalApi.subclasses = BaseV2InternalApi.subclasses + (cls,)
    async def delete_wiki_tags_v2(
        self,
        id: str,
    ) -> None:
        """Delete all tags from a wiki."""
        ...
