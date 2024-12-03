from xml.dom import NotFoundErr

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import Response

from openapi_server.apis.internal_api_base import BaseInternalApi

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")

class InternalCommentsManager(BaseInternalApi):
    async def delete_articles_comments(
        self,
        article_id: str,
    ) -> None:
        """Deletes all comments from an article"""
        result = await mongodb['comment'].delete_many({"article_id" : ObjectId(article_id)})
        if result.deleted_count == 0:
            raise NotFoundErr()
