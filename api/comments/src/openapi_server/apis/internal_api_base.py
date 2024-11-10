# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from starlette.responses import Response


class BaseInternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseInternalApi.subclasses = BaseInternalApi.subclasses + (cls,)
    async def delete_articles_comments(
        self,
        article_id: str,
    ) -> Response:
        """Deletes all comments from an article"""
        ...
