from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.apis.admins_api_base import BaseAdminsApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")
class AdminsManager(BaseAdminsApi):

    async def delete_tag(
            self,
            id: str,
    ) -> None:
        """Delete a wiki tag."""
        tag_id = ObjectId(id)
        tag = await mongodb["tag"].find_one({"_id": tag_id})

        if not tag:
            raise KeyError

        await mongodb["tag"].delete_one({"_id": tag_id})

        await mongodb["wiki"].update_many(
            {},
            {"$pull": {"tags": {"_id": tag_id}}}
        )

        await mongodb["article"].update_many(
            {},
            {"$pull": {"tags": {"_id": tag_id}}}
        )

        return {"status": "success", "message": f"Tag {id} deleted successfully"}


    async def post_wiki_tag(
            self,
            id: str,
            new_tag: NewTag
    ) -> Tag:
        """Create a new tag in a given wiki."""
        wiki_id = ObjectId(id)
        wiki = await mongodb["wiki"].find_one({"_id": wiki_id})

        if not wiki:
            raise KeyError

        tag_document = {
            "tag": new_tag.tag,
            "wiki_id": wiki_id,
            "articles": []
        }

        result = await mongodb["tag"].insert_one(tag_document)

        created_tag = await mongodb["tag"].find_one({"_id": result.inserted_id})

        await mongodb["wiki"].update_one(
            {"_id": wiki_id},
            {"$push": {"tags": {
                "_id": ObjectId(created_tag["_id"]),
                "name": created_tag["tag"]
            }}}
        )

        return Tag.from_dict({
            "id": str(created_tag["_id"]),
            "tag": created_tag["tag"],
            "wiki_id": str(created_tag["wiki_id"]),
            "articles": created_tag["articles"]
        })