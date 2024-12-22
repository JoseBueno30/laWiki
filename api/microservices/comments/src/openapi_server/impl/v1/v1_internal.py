from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import Response

from openapi_server.apis.v1.v1_internal_api_base import BaseV1InternalApi

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")
class V1InternalComments(BaseV1InternalApi):
    async def v1_delete_articles_comments(
        self,
        article_id: str,
    ) -> None:
        """Deletes all comments from an article"""
        result = await mongodb['comment'].delete_many({"article_id": ObjectId(article_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Article not found")
        return None
