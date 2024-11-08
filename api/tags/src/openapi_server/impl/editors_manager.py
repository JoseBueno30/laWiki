from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.tag_id_list import TagIDList
from openapi_server.apis.editors_api_base import BaseEditorsApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")
class EditorsManager(BaseEditorsApi):
    async def assign_tags(
            self,
            id: str,
            tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        article_id = ObjectId(id)
        tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list.tag_ids or []]

        article = await mongodb["article"].find_one({"_id": article_id}, {"title": 1})
        if not article:
            raise KeyError

        await mongodb["article"].update_one(
            {"_id": article_id},
            {"$addToSet": {
                "tags": {"$each": [
                    {"_id": tag_id, "tag": (await mongodb["tag"].find_one({"_id": tag_id}, {"tag": 1}))["tag"]}
                    for tag_id in tag_ids]}
            }}
        )

        await mongodb["tag"].update_many(
            {"_id": {"$in": tag_ids}},
            {"$addToSet": {"articles": {"_id": article_id, "name": article["title"]}}}
        )

        return {
            "status": "success",
            "assigned_tags": [str(tag_id) for tag_id in tag_ids],
            "article_id": str(article_id)
        }


    async def unassign_tags(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        article_id = ObjectId(id)

        article = await mongodb["article"].find_one({"_id": article_id}, {"title": 1})
        if not article:
            raise KeyError

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        await mongodb["article"].update_one(
            {"_id": article_id},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )

        await mongodb["tag"].update_many(
            {"_id": {"$in": tag_ids}},
            {"$pull": {"articles": {"_id": article_id}}}
        )

        return {
            "status": "success",
            "unassigned_tags": [str(tag_id) for tag_id in tag_ids],
            "article_id": str(article_id)
        }