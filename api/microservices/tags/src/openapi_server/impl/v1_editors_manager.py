from bson import ObjectId
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from openapi_server.impl import api_calls_v1
from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.apis.v1_editors_api_base import BaseV1EditorsApi

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiV2BD")
class EditorsManagerV1(BaseV1EditorsApi):

    def __init__(self):
        super().__init__()
    async def assign_tags_v1(
        self,
        id: str,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        article_id = ObjectId(id)
        tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list.tag_ids or []]

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]

        if not await api_calls_v1.check_article(id):
            raise KeyError

        article = await api_calls_v1.get_article(id)

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$addToSet": {"articles": {"_id": article_id, "name": article["title"]}}}
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": str(tag_id),
                    "tag": (await mongodb["tag"].find_one({"_id": tag_id}, {"tag": 1}))["tag"]
                }
                for tag_id in existing_tag_ids
            ]
        }

        await api_calls_v1.assign_article_tags(id, id_tags_body)

        return None


    async def delete_tag_v1(
        self,
        id: str,
    ) -> None:
        """Delete a wiki tag."""
        tag_id = ObjectId(id)
        tag = await mongodb["tag"].find_one({"_id": tag_id})

        if not tag:
            raise KeyError

        wiki_id = tag.get("wiki_id")
        articles = tag.get("articles")

        await mongodb["tag"].delete_one({"_id": tag_id})
        ids = [id]

        await api_calls_v1.unassign_wiki_tags(wiki_id, ids)

        for article in articles:
            await api_calls_v1.unassign_article_tags(article.get("_id"), ids)

        return None


    async def post_wiki_tag_v1(
        self,
        id: str,
        new_tag: NewTag,
    ) -> Tag:
        """Create a new tag in a given wiki."""
        wiki_id = ObjectId(id)

        if not await api_calls_v1.check_wiki(id):
            raise KeyError

        tag_document = {
            "tag": new_tag.tag,
            "wiki_id": wiki_id,
            "articles": [],
            "translations": {
                    "en" : "",
                    "es" : "",
                    "fr" : ""
                }
        }

        result = await mongodb["tag"].insert_one(tag_document)
        created_tag = await mongodb["tag"].find_one({"_id": result.inserted_id})

        new_tag_instance = Tag(
            id=str(created_tag["_id"]),
            tag=created_tag["tag"],
            wiki_id=str(created_tag["wiki_id"]),
            articles=created_tag["articles"]
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": new_tag_instance.id,
                    "tag": new_tag_instance.tag
                }
            ]
        }

        await api_calls_v1.assign_wiki_tags(id, id_tags_body)

        return new_tag_instance


    async def unassign_tags_v1(
        self,
        id: str,
        ids: List[str],
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        article_id = ObjectId(id)

        if not await api_calls_v1.check_article(id):
            raise KeyError

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]
        existing_tag_ids_str = [str(tag["_id"]) for tag in existing_tags]

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$pull": {"articles": {"_id": article_id}}}
        )

        await api_calls_v1.unassign_article_tags(id, existing_tag_ids_str)

        return None