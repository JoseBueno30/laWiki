# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401



class BaseInternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalApi.subclasses = BaseInternalApi.subclasses + (cls,)
    async def check_article_by_id(
        self,
        id: str,
    ) -> None:
        """Check if an Article exits given its unique ID. """
        ...
