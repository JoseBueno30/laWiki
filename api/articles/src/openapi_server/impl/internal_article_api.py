from xml.dom import NotFoundErr

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from openapi_server.apis.internal_api_base import BaseInternalApi
from openapi_server.models.article_list import ArticleList
from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body import IdTagsBody

from fastapi.responses import JSONResponse

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiDB")


class InternalArticleAPI(BaseInternalApi):

    def __init__(self):
        super().__init__()

    async def check_article_by_id(self, id: str, ):
        return await mongodb["article"].find_one({"_id": ObjectId(id)}, {"_id": 1}) is not None

    async def update_rating(self, id: str, id_ratings_body: IdRatingsBody):
        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"rating": id_ratings_body.rating}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def assign_article_tags(self, id: str, id_tags_body: IdTagsBody, ):
        tags = [{"_id": ObjectId(tag.id), "tag": tag.tag} for tag in id_tags_body.tag_ids or []]

        result = await mongodb["article"].update_one({"_id": ObjectId(id)},
                                                     {"$set": {"tags": tags}})
        if result.matched_count == 0:
            raise NotFoundErr
        return None

    async def unassign_article_tags(self, id: str, ids: list[str], ):

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        print(tag_ids)

        result = await mongodb["article"].update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )
        print(result)
        if result.matched_count == 0:
            raise NotFoundErr
        return None
