from bson import ObjectId
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v3_internal_api_base import BaseV3InternalApi

from openapi_server.apis.v2_public_api import get_wiki_tags_v2

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiV2BD")
class InternalManagerV3(BaseV3InternalApi):
    def __init__(self):
        super().__init__()

    async def delete_wiki_tags_v3(
        self,
        id: str,
    ) -> None:
        """Delete all tags from a wiki."""
        
        await mongodb["tag"].delete_many({"wiki_id" : ObjectId(id)})

        return None