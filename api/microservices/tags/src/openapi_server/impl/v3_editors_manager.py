from bson import ObjectId
from typing import List

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v3_editors_api_base import BaseV3EditorsApi
from openapi_server.impl import api_calls_v2
from openapi_server.models.new_tag_v2 import NewTagV2
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_v2 import TagV2

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiV2BD")
class EditorManagerV3(BaseV3EditorsApi):
    def __init__(self):
        super().__init__()

    async def assign_tags_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
        tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        article_id = ObjectId(id)
        tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list.tag_ids or []]

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]

        if not await api_calls_v2.check_article(id):
            raise KeyError

        article = await api_calls_v2.get_article(id)

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$addToSet": {"articles": {"_id": article_id, "name": article["title"]}}}
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": str(tag_id),
                    "tag": tag_data.get("translations", {})
                }
                for tag_id in existing_tag_ids
                for tag_data in [await mongodb["tag"].find_one({"_id": tag_id}, {"translations": 1})]
                if tag_data  
            ]
        }



        await api_calls_v2.assign_article_tags(id, id_tags_body)

        return None


    async def delete_tag_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
    ) -> None:
        """Delete a wiki tag."""

        tag_id = ObjectId(id)
        tag = await mongodb["tag"].find_one({"_id": tag_id})


        if not tag:
            raise KeyError

        wiki_id = tag.get("wiki_id")

        # Checks if the user is authorized to execute the operation
        wiki = api_calls_v2.get_wiki(wiki_id)
        if not admin and wiki['author']['_id'] != ObjectId(user_id):
            raise HTTPException(status_code=403, detail="Unauthorized")

        articles = tag.get("articles")

        await mongodb["tag"].delete_one({"_id": tag_id})
        ids = [id]

        await api_calls_v2.unassign_wiki_tags(wiki_id, ids)

        for article in articles:
            await api_calls_v2.unassign_article_tags(article.get("_id"), ids)

        return None


    async def post_wiki_tag_v3(
        self,
        id: str,
        user_id: str,
        admin: bool,
        new_tag_v2: NewTagV2,
    ) -> TagV2:
        """Create a new tag in a given wiki."""
        wiki_id = ObjectId(id)

        # Checks if the user is authorized to execute the operation
        wiki = api_calls_v2.get_wiki(id)
        if not admin and wiki['author']['_id'] != ObjectId(user_id):
            raise HTTPException(status_code=403, detail="Unauthorized")

        if not await api_calls_v2.check_wiki(id):
            raise KeyError

        if not new_tag_v2.translation:
            tag_document = {
                "tag": new_tag_v2.tag,
                "wiki_id": wiki_id,
                "articles": [],
                "translations": {
                    "en" : new_tag_v2.tag,
                    "es" : new_tag_v2.tag,
                    "fr" : new_tag_v2.tag
                }
            }
        else: # The original tag needs to be translated into the other languages
            english = await api_calls_v2.translate(new_tag_v2.tag, new_tag_v2.lan, "en")
            spanish = await api_calls_v2.translate(new_tag_v2.tag, new_tag_v2.lan, "es")
            french = await api_calls_v2.translate(new_tag_v2.tag, new_tag_v2.lan, "fr")
            tag_document = {
                "tag": new_tag_v2.tag,
                "wiki_id": wiki_id,
                "articles": [],
                "translations": {
                    "en": english["translatedText"],
                    "es": spanish["translatedText"],
                    "fr": french["translatedText"]
                }
            }

        result = await mongodb["tag"].insert_one(tag_document)
        created_tag = await mongodb["tag"].find_one({"_id": result.inserted_id})

        new_tag_instance = TagV2(
            id=str(created_tag["_id"]),
            tag=created_tag["tag"],
            wiki_id=str(created_tag["wiki_id"]),
            articles=created_tag["articles"],
            translations=created_tag["translations"]
        )

        id_tags_body = {
            "tag_ids": [
                {
                    "id": new_tag_instance.id,
                    "tag": new_tag_instance.translations
                }
            ]
        }

        await api_calls_v2.assign_wiki_tags(id, id_tags_body)

        return new_tag_instance


    async def unassign_tags_v3(
        self,
        id: str,
        ids: list[str],
        user_id: str,
        admin: str,
    ) -> None:
        """Unassigns a list of tags, given their IDs to an article."""
        article_id = ObjectId(id)

        if not await api_calls_v2.check_article(id):
            raise KeyError

        tag_ids = [ObjectId(tag_id) for tag_id in ids or []]

        existing_tags = await mongodb["tag"].find({"_id": {"$in": tag_ids}}).to_list(length=None)
        existing_tag_ids = [tag["_id"] for tag in existing_tags]
        existing_tag_ids_str = [str(tag["_id"]) for tag in existing_tags]

        await mongodb["tag"].update_many(
            {"_id": {"$in": existing_tag_ids}},
            {"$pull": {"articles": {"_id": article_id}}}
        )

        await api_calls_v2.unassign_article_tags(id, existing_tag_ids_str)

        return None