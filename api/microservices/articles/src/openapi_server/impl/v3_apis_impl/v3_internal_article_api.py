from typing import Optional, List
from xml.dom import NotFoundErr

from bson import ObjectId
from pydantic import StrictStr, StrictBool, Field

from openapi_server.apis.v3_internal_api_base import BaseV3InternalApi
from openapi_server.impl.utils.functions import mongodb
from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2


class InternalArticleAPIV3(BaseV3InternalApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def assign_article_tags_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        id_tags_body_v2: Optional[IdTagsBodyV2],
    ) -> None:

        if not admin and not user_id:
            raise Exception("Unauthorized")

        tags = [{"_id": ObjectId(tag.id), "tag": tag.tag} for tag in id_tags_body_v2.tag_ids or []]

        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"tags": tags}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def check_article_by_idv3(
        self,
        id: StrictStr,
    ) -> None:
        return await mongodb["article"].find_one(filter={"_id": ObjectId(id)}) is not None

    async def unassign_article_tags_v3(
        self,
        id: StrictStr,
        ids: List[StrictStr],
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:

        if not admin and not user_id:
            raise Exception("Unauthorized")

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        print(tag_ids)

        result = await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def update_rating_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
        id_ratings_body_v2: Optional[IdRatingsBodyV2],
    ) -> None:

        if not admin and not user_id:
            raise Exception("Unauthorized")

        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"rating": id_ratings_body_v2.rating}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def delete_articles_from_wiki_v3(
        self,
        id: StrictStr,
        user_id: StrictStr,
        admin: StrictBool,
    ) -> None:

        if not admin:
            raise Exception("Unauthorized")

        pipeline = [
            {
                "$match": {
                    "wiki_id": ObjectId(id)
                }
            },
            {
                "$project": {
                    "_id": 1
                }
            }
        ]

        id_list = await mongodb["article"].aggregate(pipeline).to_list(None)

        for article_id in id_list:
            await BaseV3InternalApi.subclasses[0]().delete_articles_from_wiki(article_id, user_id, admin)


        return None