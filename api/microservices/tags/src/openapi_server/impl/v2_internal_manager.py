from bson import ObjectId
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v2_internal_api_base import BaseV2InternalApi
from openapi_server.impl import api_calls_v2

from openapi_server.apis.v1_public_api import get_wiki_tags_v1

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiV2BD")
class InternalManagerV2(BaseV2InternalApi):
    def __init__(self):
        super().__init__()

    async def delete_wiki_tags_v2(
        self,
        id: str,
    ) -> None:
        """Delete all tags from a wiki."""
        wiki_id = ObjectId(id)

        if not await api_calls_v2.check_wiki(id):
            raise KeyError

        tags_data = await api_calls_v2.get_wiki_tags(id)
        tags = tags_data.get("articles", [])

        for tag in tags:
            tag_id = tag["id"]
            articles = tag.get("articles", [])
            
            for article in articles:
                article_id = article["id"]
                await api_calls_v2.unassign_article_tags(article_id, [tag_id])

            await mongodb["tag"].delete_one({"_id": ObjectId(tag_id)})

        return