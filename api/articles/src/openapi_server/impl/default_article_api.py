from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.article_version import ArticleVersion

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiDB")

transform_article_ids_pipeline = [
    {"$addFields": {
        "id": {"$toString": "$_id"},
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
        },
        "versions": {
                "$map": {
                    "input": "$versions",
                    "as": "version",
                    "in": {
                        "id": {"$toString": "$$version._id"},
                        "title": "$$version.title",
                        "modification_date": "$$version.modification_date",
                        "author" : {
                            "id": {"$toString": "$$version.author._id"},
                            "name": "$$version.author.name"
                        }
                    }
                }
            },
        "wiki_id":{"$toString":"$wiki_id"}
    }},
    {"$unset": ["_id", "author._id", "tags._id", "versions._id", "versions.autor._id"]}  # Quita los campos _id originales
]

transform_version_ids_pipeline = [
    {"$addFields": {
        "id": {"$toString": "$_id"},
        "article_id": {"$toString": "$article_id"},
        "author.id": {
            "$toString": "$author._id"},
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

class ArticleAPI(BaseDefaultApi):


    def __init__(self):
        super().__init__()

    async def get_article_by_id(self, id: str,):
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_article_ids_pipeline
        ]

        # Ejecutar la consulta de agregación
        article = await mongodb["article"].aggregate(pipeline).to_list(length=1)

        # Verificar si se encontró el artículo
        if not article[0]:
            raise Exception

        return article[0]  # El resultado es una lista, así que se toma el primer elemento

    async def get_article_by_name(self, name: str, wiki_id: str):
        #TODO: Throw InvalidaParameterValue if name is not valid
        version_id_pipeline = [
            {
                '$match': {
                    "title": name,
                    "wiki_id": ObjectId(wiki_id)
                }
            }, {
                '$unwind': '$versions'
            }, {
                '$sort': {
                    'versions.modification_date': -1
                }
            }, {
                '$group': {
                    '_id': '$_id',
                    'latestVersion': {
                        '$first': '$versions'
                    }
                }
            }, {
                '$project': {
                    '_id': '$latestVersion._id'
                }
            }
        ]

        print(version_id_pipeline)


        version_ObjectId = await mongodb["article"].aggregate(version_id_pipeline).to_list(length=1)

        print(version_ObjectId)
        print(version_ObjectId[0]["_id"])

        if not version_ObjectId[0]:
            raise Exception

        version_pipeline = [
            {
                '$match': {
                    '_id': version_ObjectId[0]["_id"],

                }
            },
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(version_pipeline).to_list(length=1)

        if not article_version[0]:
            raise Exception

        return article_version[0]
