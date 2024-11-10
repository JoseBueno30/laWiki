from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.impl import api_calls
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

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]

        if not await api_calls.check_article(id):
            raise KeyError

        article = await api_calls.get_article(id)

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$addToSet": {"articles": {"_id": article_id, "name": article["title"]}}}
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": str(tag_id),
                    "tag": (await mongodb["tag"].find_one({"_id": tag_id}, {"tag": 1}))["tag"]
                }
                for tag_id in existing_tag_ids
            ]
        }

        await api_calls.assign_article_tags(id, id_tags_body)

        return None


    async def unassign_tags(
        self,
        id: str,
        ids: list[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        article_id = ObjectId(id)

        if not await api_calls.check_article(id):
            raise KeyError

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]
        existing_tag_ids_str = [str(tag["_id"]) for tag in existing_tags]

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$pull": {"articles": {"_id": article_id}}}
        )

        await api_calls.unassign_article_tags(id, existing_tag_ids_str)

        return None