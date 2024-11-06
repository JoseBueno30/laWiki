from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.article_version import ArticleVersion

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiDB")

class ArticleAPI(BaseDefaultApi):

    def __init__(self):
        super().__init__()

    async def get_article_by_id(self, id: str,):
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            {"$addFields": {
                "id": {"$toString": "$_id"},
                "article_id": {"$toString": "$article_id"},
                "author.id": {"$toString": "$author._id"},
                "tags": {
                    "$map": {
                        "input": "$tags",
                        "as": "tag",
                        "in": {
                            "id": {"$toString": "$$tag._id"},
                            "tag": "$$tag.tag"
                        }
                    }
                }
            }},
            {"$unset": ["_id", "author._id", "tags._id"]}  # Quita los campos _id originales
        ]

        # Ejecutar la consulta de agregación
        article = await mongodb["article_version"].aggregate(pipeline).to_list(length=1)

        # Verificar si se encontró el artículo
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        return article[0]  # El resultado es una lista, así que se toma el primer elemento
