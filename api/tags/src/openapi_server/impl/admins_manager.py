from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.impl import api_calls
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

        wiki_id = tag.get("wiki_id")
        articles = tag.get("articles")

        await mongodb["tag"].delete_one({"_id": tag_id})
        ids = [id]

        await api_calls.unassign_wiki_tags(wiki_id, ids)

        for article in articles:
            await api_calls.unassign_article_tags(article.get("_id"), ids)

        return None

    async def post_wiki_tag(
            self,
            id: str,
            new_tag: NewTag
    ) -> Tag:
        """Create a new tag in a given wiki."""
        wiki_id = ObjectId(id)

        if not await api_calls.check_wiki(id):
            raise KeyError

        tag_document = {
            "tag": new_tag.tag,
            "wiki_id": wiki_id,
            "articles": []
        }

        result = await mongodb["tag"].insert_one(tag_document)
        created_tag = await mongodb["tag"].find_one({"_id": result.inserted_id})

        new_tag_instance = Tag(
            id=str(created_tag["_id"]),
            tag=created_tag["tag"],
            wiki_id=str(created_tag["wiki_id"]),
            articles=created_tag["articles"]
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": new_tag_instance.id,
                    "name": new_tag_instance.tag
                }
            ]
        }

        await api_calls.assign_wiki_tags(id, id_tags_body)

        return new_tag_instance