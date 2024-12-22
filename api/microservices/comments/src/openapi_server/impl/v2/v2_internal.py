from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import Response

from openapi_server.apis.v2.v2_internal_api_base import BaseV2InternalApi

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")
class V2InternalComments(BaseV2InternalApi):
    async def v2_delete_articles_comments(
        self,
        article_id: str,
    ) -> None:
        """Deletes all comments from an article"""
        result = await mongodb['comment'].delete_many({"article_id": ObjectId(article_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return None