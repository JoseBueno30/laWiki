from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
from openapi_server.impl import api_calls
from openapi_server.models.tag_list_v2 import TagListV2
from openapi_server.models.tag_v2 import TagV2

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiV2BD")
class PublicManagerV2(BaseV2PublicApi):
    def __init__(self):
        super().__init__()

    async def get_articles_tags_v2(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagListV2:
        """Retrieves all the tags from an article."""
        article_id = ObjectId(id)

        if not await api_calls.check_article(id):
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
                    },
                    "translations": {
                        "en": "$translations.en",
                        "es": "$translations.es",
                        "fr": "$translations.fr",
                        "it": "$translations.it"
                    }
                }
            }
        ]

        result = await mongodb["tag"].aggregate(pipeline).to_list(None)

        return TagListV2(
            articles=[TagV2.from_dict(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )


    async def get_tag_v2(
        self,
        id: str,
    ) -> TagV2:
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
                    },
                    "translations": {
                        "en": "$translations.en",
                        "es": "$translations.es",
                        "fr": "$translations.fr",
                        "it": "$translations.it"
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

        return TagV2.from_dict(tag_data[0])


    async def get_wiki_tags_v2(
        self,
        id: str,
        limit: int,
        offset: int,
    ) -> TagListV2:
        """Retrieve all the tags from a wiki."""
        wiki_id = ObjectId(id)

        if not await api_calls.check_wiki(id):
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
                    },
                    "translations": {
                        "en": "$translations.en",
                        "es": "$translations.es",
                        "fr": "$translations.fr",
                        "it": "$translations.it"
                    }
                }
            }
        ]

        result = await mongodb["tag"].aggregate(pipeline).to_list(None)

        return TagListV2(
            articles=[TagV2.from_dict(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )