from xml.dom import NotFoundErr

from bson import ObjectId
from typing import List

from openapi_server.apis.v2_internal_api_base import BaseV2InternalApi
from openapi_server.impl.utils.functions import mongodb
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
        tags = [{"_id": ObjectId(tag.id), "tag": tag.tag} for tag in id_tags_body_v2.tag_ids or []]

        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"tags": tags}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def check_article_by_idv2(
        self,
        id: str,
    ) -> None:
        return await mongodb["article"].find_one(filter={"_id": ObjectId(id)}) is not None

    async def unassign_article_tags_v2(
        self,
        id: str,
        ids: List[str],
    ) -> None:

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        print(tag_ids)

        result = await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def update_rating_v2(
        self,
        id: str,
        id_ratings_body_v2: IdRatingsBodyV2,
    ) -> None:
        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"rating": id_ratings_body_v2.rating}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def delete_articles_from_wiki(
        self,
        id: str
    ) -> None:

        pipeline = [
            {
                "$match":{
                    "wiki_id": ObjectId(id)
                }
            },
            {
                "$project":{
                    "_id": 1
                }
            }
        ]

        id_list = await mongodb["article"].aggregate(pipeline).to_list(None)

        for article_id in id_list:
            async with httpx.AsyncClient() as client:
                await client.delete(f"http://{ARTICLES_URL}:{ARTICLES_PORT}/articles/{str(article_id)}")

        return None