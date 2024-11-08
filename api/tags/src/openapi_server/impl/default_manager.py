from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.tag import Tag
from openapi_server.models.tag_list import TagList
from openapi_server.apis.default_api_base import BaseDefaultApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")
class DefaultManager(BaseDefaultApi):
    async def get_articles_tags(
            self,
            id: str,
            limit: int,
            offset: int
    ) -> TagList:
        """Retrieves all the tags from an article and returns them with full details."""

        article_id = ObjectId(id)

        article = await mongodb["article"].find_one({"_id": article_id})
        if not article:
            raise KeyError

        total_tags = len(article.get("tags", []))

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
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )


    async def get_tag(
            self,
            id: str,
    ) -> Tag:
        """Get a tag by ID."""
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


    async def get_wiki_tags(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagList:
        """Retrieve all the tags from a wiki."""
        wiki_id = ObjectId(id)

        wiki = await mongodb["wiki"].find_one({"_id": wiki_id})
        if not wiki:
            raise KeyError

        total_tags = len(wiki.get("tags", []))

        pipeline = [
            {"$match": {"articles._id": wiki_id}},

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
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )