# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictBool, StrictStr
from typing import Any, Optional
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2


class BaseV3EditorsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV3EditorsApi.subclasses = BaseV3EditorsApi.subclasses + (cls,)
    async def create_article_v3(
        self,
        user_id: StrictStr,
        admin: StrictBool,
        new_article_v2: Optional[NewArticleV2],
    ) -> ArticleV2:
        """Create a new Article in a given wiki"""
        ...


    async def create_article_version_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        new_article_version_v2: Optional[NewArticleVersionV2],
    ) -> ArticleVersionV2:
        """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
        ...


    async def delete_article_by_idv3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        """Delete an Article identified by it&#39;s unique ID"""
        ...


    async def delete_article_version_by_id_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        """Delete an ArticleVersion identified by it&#39;s unique ID"""
        ...


    async def restore_article_version_v3(
        self,
        article_id: StrictStr,
        version_id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:
        """Restore an older ArticleVersion of an Article."""
        ...
