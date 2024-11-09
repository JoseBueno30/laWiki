from typing import List

from bson import ObjectId

from openapi_server.apis.default_api_base import BaseDefaultApi
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_list import TagList

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")

class TagsManager(BaseDefaultApi):

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

    async def delete_tag(
        self,
        id: str,
    ) -> None:
        """Delete a wiki tag."""
        tag_id = ObjectId(id)
        tag = await mongodb["tag"].find_one({"_id": tag_id})

        if not tag:
            raise KeyError

        await mongodb["tag"].delete_one({"_id": tag_id})

        await mongodb["wiki"].update_many(
            {},
            {"$pull": {"tags": {"_id": tag_id}}}
        )

        await mongodb["article"].update_many(
            {},
            {"$pull": {"tags": {"_id": tag_id}}}
        )

        return {"status": "success", "message": f"Tag {id} deleted successfully"}

    async def post_wiki_tag(
            self,
            id: str,
            new_tag: NewTag
    ) -> Tag:
        """Create a new tag in a given wiki."""
        wiki_id = ObjectId(id)
        wiki = await mongodb["wiki"].find_one({"_id": wiki_id})

        if not wiki:
            raise KeyError

        tag_document = {
            "tag": new_tag.tag,
            "wiki_id": wiki_id,
            "articles": []
        }

        result = await mongodb["tag"].insert_one(tag_document)

        created_tag = await mongodb["tag"].find_one({"_id": result.inserted_id})

        await mongodb["wiki"].update_one(
            {"_id": wiki_id},
            {"$push": {"tags": {
                "_id": ObjectId(created_tag["_id"]),
                "name": created_tag["tag"]
            }}}
        )

        return Tag.from_dict({
            "id": str(created_tag["_id"]),
            "tag": created_tag["tag"],
            "wiki_id": str(created_tag["wiki_id"]),
            "articles": created_tag["articles"]
        })

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
            {
                "$match": {
                    "_id": wiki_id
                }
            },
            {
                "$lookup": {
                    "from": "tag",
                    "localField": "tags._id",
                    "foreignField": "_id",
                    "as": "full_tags"
                }
            },
            {
                "$unwind": "$full_tags"
            },
            {
                "$lookup": {
                    "from": "article",
                    "localField": "full_tags._id",
                    "foreignField": "tags._id",
                    "as": "articles"
                }
            },
            {
                "$skip": offset
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": 0,
                    "id": {"$toString": "$full_tags._id"},
                    "tag": "$full_tags.tag",
                    "wiki_id": {"$toString": "$full_tags.wiki_id"},
                    "articles": {
                        "$map": {
                            "input": "$articles",
                            "as": "article",
                            "in": {
                                "_id": 0,
                                "id": {"$toString": "$$article._id"},
                                "name": "$$article.title"
                            }
                        }
                    }
                }
            }
        ]

        result = await mongodb["wiki"].aggregate(pipeline).to_list(None)

        return TagList(
            articles=[Tag.from_dict(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )

    async def get_articles_tags(
            self,
            id: str,
            limit: int,
            offset: int
    ) -> TagList:
        """Retrieves all the tags from an article and returns them with full details."""

        # Convertir el ID del artículo en un ObjectId compatible con MongoDB
        article_id = ObjectId(id)

        # Verificar si el artículo existe en la base de datos
        article = await mongodb["article"].find_one({"_id": article_id})
        if not article:
            raise KeyError("El artículo no existe")

        # Contar el total de tags asociados al artículo
        total_tags = len(article.get("tags", []))

        # Pipeline de agregación para obtener los tags asociados al artículo
        pipeline = [
            # Filtrar tags que contienen el artículo especificado en su lista de artículos
            {"$match": {"articles._id": article_id}},

            # Aplicar paginación con skip y limit
            {"$skip": offset},
            {"$limit": limit},

            # Proyectar el resultado en el formato requerido
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

        # Ejecutar el pipeline de agregación
        result = await mongodb["tag"].aggregate(pipeline).to_list(None)

        # Construir y retornar el objeto TagList con los resultados paginados
        return TagList(
            articles=[Tag.model_validate(tag) for tag in result],
            total=total_tags,
            offset=offset,
            limit=limit,
            previous=None if offset == 0 else f"/tags?offset={max(0, offset - limit)}&limit={limit}",
            next=None if offset + limit >= total_tags else f"/tags?offset={offset + limit}&limit={limit}"
        )


    async def assign_tags(
            self,
            id: str,
            tag_id_list: TagIDList,
    ) -> None:
        """Assigns a list of tags, given their IDs, to an article."""
        article_id = ObjectId(id)
        tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list.tag_ids or []]

        article = await mongodb["article"].find_one({"_id": article_id}, {"title": 1})
        if not article:
            raise KeyError

        await mongodb["article"].update_one(
            {"_id": article_id},
            {"$addToSet": {
                "tags": {"$each": [
                    {"_id": tag_id, "tag": (await mongodb["tag"].find_one({"_id": tag_id}, {"tag": 1}))["tag"]}
                    for tag_id in tag_ids]}
            }}
        )

        await mongodb["tag"].update_many(
            {"_id": {"$in": tag_ids}},
            {"$addToSet": {"articles": {"_id": article_id, "name": article["title"]}}}
        )

        return {
            "status": "success",
            "assigned_tags": [str(tag_id) for tag_id in tag_ids],
            "article_id": str(article_id)
        }

    async def unassign_tags(
            self,
            id: str,
            tag_id_list: TagIDList,
    ) -> None:
        """Unassigns a list of tags, given their IDs from an article."""
        article_id = ObjectId(id)

        article = await mongodb["article"].find_one({"_id": article_id}, {"title": 1})
        if not article:
            raise KeyError

        tag_ids = [ObjectId(tag_id) for tag_id in tag_id_list.tag_ids or []]

        await mongodb["article"].update_one(
            {"_id": article_id},
            {"$pull": {"tags": {"_id": {"$in": tag_ids}}}}
        )

        await mongodb["tag"].update_many(
            {"_id": {"$in": tag_ids}},
            {"$pull": {"articles": {"_id": article_id}}}
        )

        return {
            "status": "success",
            "unassigned_tags": [str(tag_id) for tag_id in tag_ids],
            "article_id": str(article_id)
        }