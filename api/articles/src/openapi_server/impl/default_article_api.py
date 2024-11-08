from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models import tag
from openapi_server.models.article_list import ArticleList

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

class DefaultArticleAPI(BaseDefaultApi):


    def __init__(self):
        super().__init__()

    async def get_article_by_id(self, id: str,):
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_article_ids_pipeline
        ]

        article = await mongodb["article"].aggregate(pipeline).to_list(length=1)

        if not article[0]:
            raise Exception

        return article[0]

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

    async def get_article_version_by_id(self, id: str,):
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(pipeline).to_list(length=1)

        print(article_version)

        if not article_version[0]:
            raise Exception

        return article_version[0]

    async def get_article_by_author(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleList:

        total_documents = await mongodb["article"].count_documents({})
        print("total: ",total_documents)

        pipeline = [
            {
                "$match": {
                    "author._id": ObjectId(id)
                }
            },
            {
                "$sort": {
                    "creation_date": -1 if order == "recent" else 1
                }
            },
            {
                "$skip": offset
            },
            {
                "$limit": limit
            },
            *transform_article_ids_pipeline,
            {
                "$group": {
                    "_id": None,
                    "articles":{
                        "$push": "$$ROOT"
                    }
                }
            },
            {
                "$addFields": {
                    "total": {
                        "$size": "$articles"
                    },
                    "offset": offset,
                    "limit": limit,
                    "next":{
                        "$cond":{
                            "if": {"$lt":[offset + limit, total_documents]},
                            "then": f"/articles/?offset={offset + limit}&limit={limit}",
                            "else": None
                        }
                    },
                    "previous":{
                        "$cond":{
                            "if": {"$gt":[offset, 0]},
                            "then": f"/articles/?offset={max(offset - limit, 0)}&limit={limit}",
                            "else": None
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                }
            }

        ]

        articles = await mongodb["article"].aggregate(pipeline).to_list()

        if not articles[0]:
            raise Exception

        return articles[0]

    async def search_articles(
        self,
        wiki_id: str,
        name: str,
        tags: list[str],
        offset: int,
        limit: int,
        order: str,
        creation_date: str,
        author_name: str,
        editor_name: str,
    ) -> ArticleList:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        matching_variables = {}
        if wiki_id is not None:
            matching_variables["wiki_id"] = ObjectId(wiki_id)
        if name is not None:
            matching_variables["title"] = name
        if creation_date is not None:
            dates = creation_date.split("-")
            if len(dates) == 1:
                matching_variables["creation_date"] = datetime.strptime(dates[0], "%Y/%m/%d")
            elif len(dates) == 2:
                matching_variables["creation_date"] = {
                    "$gte": datetime.strptime(dates[0], "%Y/%m/%d"),
                    "$lte": datetime.strptime(dates[1], "%Y/%m/%d")
                }
        if author_name is not None:
            matching_variables["author.name"] = author_name
        if editor_name is not None:
            matching_variables["versions.author.name"] = editor_name

        if tags is not None:
            tag_ids = [ObjectId(tag["id"]) for tag in tags]
            matching_variables["tags._id"] = {"$all": tag_ids}

        total_count = await mongodb['article'].count_documents(matching_variables)

        sorting_variables = {"rating" : -1}

        if order == "recent":
            sorting_variables["creation_date"] = {-1}
        elif order == "oldest":
            sorting_variables["creation_date"] = {1}
        elif order == "popular":
            sorting_variables["rating"] = {-1}
        elif order == "unpopular":
            sorting_variables["rating"] = {1}

        group_articles_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "articles": {
                        "$push": "$$ROOT"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                }
            }
        ]

        print("AAAAAAAA")


        #TODO: arreglar el total
        pagination_pipeline = [
            {
                "$addFields": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "next": {
                        "$cond": {
                            "if": {"$lt": [offset + limit, total_count]},
                            "then": f"/articles/?offset={offset + limit}&limit={limit}",
                            "else": None
                        }
                    },
                    "previous": {
                        "$cond": {
                            "if": {"$gt": [offset, 0]},
                            "then": f"/articles/?offset={max(offset - limit, 0)}&limit={limit}",
                            "else": None
                        }
                    },
                }
            }
        ]

        query_pipeline = [
            {"$match": matching_variables},
            {"$sort": sorting_variables},
            {"$skip": offset},
            {"$limit": limit},
            *transform_article_ids_pipeline,
            *group_articles_pipeline,
            *pagination_pipeline
        ]

        print(query_pipeline)

        articles = await mongodb["article"].aggregate(query_pipeline).to_list()

        print(articles)

        if not articles:
            raise Exception

        return articles[0]
