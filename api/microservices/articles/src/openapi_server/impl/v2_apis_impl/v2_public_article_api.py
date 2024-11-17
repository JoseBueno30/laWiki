from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
from openapi_server.models.models_v2.article_list_v2 import ArticleListV2
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_list_v2 import ArticleVersionListV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.inline_response200_v2 import InlineResponse200V2


class PublicArticleAPIV2(BaseV2PublicApi):

    def __init__(self):
        super().__init__()

    async def get_article_by_id_v2(
        self,
        id: str,
    ) -> ArticleV2:
        return None

    async def get_article_by_name_v2(
        self,
        name: str,
        wiki: str,
    ) -> ArticleVersionV2:
        return None

    async def get_article_version_list_by_article_idv2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionListV2:
        return None

    async def get_article_version_by_id_v2(
        self,
        id: str,
        lan: str,
    ) -> ArticleVersionV2:
        return None

    async def get_article_by_author_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        return None

    async def get_article_version_body_by_idv2(
        self,
        id: str,
        parsed: bool,
        lan: str,
    ) -> InlineResponse200V2:
        return None

    async def get_articles_commented_by_user_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        return None

    async def search_articles_v2(
        self,
        wiki_id: str,
        name: str,
        tags: list[str],
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        editor_name: str,
    ) -> ArticleListV2:
        return None