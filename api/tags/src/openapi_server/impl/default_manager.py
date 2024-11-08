from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from src.openapi_server.apis.default_api_base import BaseDefaultApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")
class DefaultManager(BaseDefaultApi):
    async def get_articles_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieves all the tags from an article."""
        ...


    async def get_tag(
            self,
            id: str,
    ) -> Tag:
        """Get a tag by ID."""
        object_id = ObjectId(id)
        pipeline = [
            {
                "$match": {
                    "_id": object_id
                }
            },
            {
                "$addFields": {
                    "id": {"$toString": "$_id"},
                    "wiki_id": {"$toString": "$wiki_id"},
                    "articles": {
                        "$map": {
                            "input": "$articles",
                            "as": "article",
                            "in": {
                                "id": {"$toString": "$$article._id"},
                                "name": "$$article.name"
                            }
                        }
                    }
                }
            },
            {
                "$unset": ["_id", "articles._id"]
            }
        ]

        tag_data = await mongodb["tag"].aggregate(pipeline).to_list(length=1)

        if not tag_data:
            raise KeyError

        return Tag.from_dict(tag_data[0])


    async def get_wiki_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        ...