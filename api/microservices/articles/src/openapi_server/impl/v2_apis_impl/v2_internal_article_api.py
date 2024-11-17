from openapi_server.apis.v2_internal_api_base import BaseV2InternalApi
from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2


class InternalArticleAPIV2(BaseV2InternalApi):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def assign_article_tags_v2(
        self,
        id: str,
        id_tags_body_v2: IdTagsBodyV2,
    ) -> None:
        return None

    async def check_article_by_idv2(
        self,
        id: str,
    ) -> None:
        return None

    async def unassign_article_tags_v2(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        return None

    async def update_rating_v2(
        self,
        id: str,
        id_ratings_body_v2: IdRatingsBodyV2,
    ) -> None:
        return None

    async def delete_articles_from_wiki(
        self,
        id: str
    ) -> None:
        return None