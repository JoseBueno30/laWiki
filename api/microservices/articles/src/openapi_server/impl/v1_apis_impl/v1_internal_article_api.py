from xml.dom import NotFoundErr

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


from openapi_server.apis.v1_internal_api_base import BaseV1InternalApi
from openapi_server.models.models_v1.id_ratings_body_v1 import IdRatingsBodyV1
from openapi_server.models.models_v1.id_tags_body_v1 import IdTagsBodyV1

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiDB")


class InternalArticleAPI(BaseV1InternalApi):

    def __init__(self):
        super().__init__()

    async def check_article_by_idv1(self, id: str, ):
        return await mongodb["article"].find_one({"_id": ObjectId(id)}, {"_id": 1}) is not None

    async def update_rating_v1(self, id: str, id_ratings_body: IdRatingsBodyV1):
        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"rating": id_ratings_body.rating}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def assign_article_tags_v1(self, id: str, id_tags_body: IdTagsBodyV1):
        tags = [{"_id": ObjectId(tag.id), "tag": tag.tag} for tag in id_tags_body.tag_ids or []]

        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"tags": tags}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def unassign_article_tags_v1(self, id: str, ids: List[str]):

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        print(tag_ids)

        result = await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )
        if result.matched_count == 0:
            raise NotFoundErr
        return None
