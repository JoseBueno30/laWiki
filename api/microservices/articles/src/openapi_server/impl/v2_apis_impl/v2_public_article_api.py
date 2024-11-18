from bson import ObjectId

from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
from openapi_server.impl.utils.functions import transform_article_ids_pipeline, mongodb, transform_version_ids_pipeline
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

        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_article_ids_pipeline
        ]

        article = await mongodb["article"].aggregate(pipeline).to_list(length=1)

        if not article[0]:
            raise Exception

        return article[0]

    async def get_article_by_name_v2(
        self,
        name: str,
        wiki: str,
        lan: str
    ) -> ArticleVersionV2:

        match_stage = {"wiki_id": ObjectId(wiki)}

        #   TODO Cambar especificacion para que sea con ccualquier idioma si lan es none
        if not lan:
            match_stage["$or"] = [
                {"title.en": name},
                {"title.es": name},
                {"title.fr": name}
            ]
        else:
            match_stage["title."+lan] = name

        version_id_pipeline = [
            {
                '$match': match_stage
            }, {
                '$unwind': '$versions'
            }, {
                '$sort': {
                    'versions.modification_date': -1
                }
            }, {
                '$group': {
                    '_id': '$_id',
                    'latestVersion': {
                        '$first': '$versions'
                    }
                }
            }, {
                '$project': {
                    '_id': '$latestVersion._id'
                }
            }
        ]

        print(version_id_pipeline)

        version_object_id = await mongodb["article"].aggregate(version_id_pipeline).to_list(length=1)

        if not version_object_id[0]:
            raise Exception

        version_pipeline = [
            {
                '$match': {
                    '_id': version_object_id[0]["_id"],
                }
            },
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(version_pipeline).to_list(length=1)

        if not article_version[0]:
            raise Exception

        return article_version[0]

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