from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.article_version import ArticleVersion

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiDB")

class ArticleAPI(BaseDefaultApi):

    def __init__(self):
        super().__init__()

    async def get_article_by_id(self, id: str,) -> ArticleVersion:
        article = await mongodb["article"].find_one({"_id": ObjectId(id)})

        return article
