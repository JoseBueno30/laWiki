from bson import ObjectId
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.impl import api_calls_v1
from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from openapi_server.apis.v1_public_api_base import BaseV1PublicApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")
class PublicManagerV1(BaseV1PublicApi):

    def __init__(self):
        super().__init__()
    async def get_articles_tags_v1(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieves all the tags from an article."""
        article_id = ObjectId(id)

        if not await api_calls_v1.check_article(id):
            raise KeyError

        total_tags = await mongodb["tag"].count_documents({"articles._id": article_id})

        pipeline = [
            {"$match": {"articles._id": article_id}},

            {"$skip": offset},
            {"$limit": limit},

            {
                "$project": {
                    "_id": 0,
                    "id": {"$toString": "$_id"},
                    "tag": 1,
                    "wiki_id": {"$toString": "$wiki_id"},
                    "articles": {
                        "$map": {
                            "input": "$articles",
                            "as": "article",
                            "in": {
                                "_id": 0,
                                "id": {"$toString": "$$article._id"},
                                "name": "$$article.name"
                            }
                        }
                    }
                }
            }
        ]

        result = await mongodb["tag"].aggregate(pipeline).to_list(None)

        return TagList(
            articles=[Tag.from_dict(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"v1/tags/articles/{id}?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"v1/tags/articles/{id}?offset={offset + limit}&limit={limit}"
        )


    async def get_tag_v1(
        self,
        id: str,
    ) -> Tag:
        """Get a tag by ID. """
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


    async def get_wiki_tags_v1(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        wiki_id = ObjectId(id)

        if not await api_calls_v1.check_wiki(id):
            raise KeyError

        total_tags = await mongodb["tag"].count_documents({"wiki_id": wiki_id})

        pipeline = [
            {"$match": {"wiki_id": wiki_id}},

            {"$skip": offset},
            {"$limit": limit},

            {
                "$project": {
                    "_id": 0,
                    "id": {"$toString": "$_id"},
                    "tag": 1,
                    "wiki_id": {"$toString": "$wiki_id"},
                    "articles": {
                        "$map": {
                            "input": "$articles",
                            "as": "article",
                            "in": {
                                "_id": 0,
                                "id": {"$toString": "$$article._id"},
                                "name": "$$article.name"
                            }
                        }
                    }
                }
            }
        ]

        result = await mongodb["tag"].aggregate(pipeline).to_list(None)

        return TagList(
            articles=[Tag.from_dict(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"v1/tags/wikis/{id}?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"v1/tags/wikis/{id}?offset={offset + limit}&limit={limit}"
        )
