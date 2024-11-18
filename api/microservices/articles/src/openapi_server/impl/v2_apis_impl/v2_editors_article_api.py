from openapi_server.apis.v2_editors_api_base import BaseV2EditorsApi
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2


class EditorsArticleAPIV2(BaseV2EditorsApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def create_article_v2(
        self,
        new_article_v2: NewArticleV2,
    ) -> ArticleV2:

        return None

    async def create_article_version_v2(
        self,
        id: str,
        new_article_version_v2: NewArticleVersionV2,
    ) -> ArticleVersionV2:
        return None

    async def delete_article_by_idv2(
        self,
        id: str,
    ) -> None:
        return None

    async def delete_article_version_by_id_v2(
        self,
        id: str,
    ) -> None:
        return None

    async def restore_article_version_v2(
        self,
        article_id: str,
        version_id: str,
    ) -> None:
        return None