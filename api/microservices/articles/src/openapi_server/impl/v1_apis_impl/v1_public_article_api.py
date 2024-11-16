from datetime import datetime
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
from openapi_server.impl.api_calls import get_user_comments
from openapi_server.models.models_v1.article_list_v1 import ArticleListV1
from openapi_server.models.models_v1.article_v1 import ArticleV1
from openapi_server.models.models_v1.article_version_list_v1 import ArticleVersionListV1
from openapi_server.models.models_v1.article_version_v1 import ArticleVersionV1

mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiV2BD")

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
                    "author": {
                        "id": {"$toString": "$$version.author._id"},
                        "name": "$$version.author.name"
                    }
                }
            }
        },
        "wiki_id": {"$toString": "$wiki_id"}
    }},
    {"$unset": ["_id", "author._id", "tags._id", "versions._id", "versions.autor._id"]}
    # Quita los campos _id originales
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


async def get_total_number_of_documents(collection, match_query):
    return await collection.count_documents(match_query)

def get_original_article_title(article):
    article_returned = article
    article_returned["title"] = article_returned["title"][article_returned["lan"]]
    for version in article_returned["versions"]:
        version["title"] = version["title"][article_returned["lan"]]

    return article_returned

def get_original_article_version_title(article):
    version_returned = article
    version_returned["title"] = version_returned["title"][version_returned["lan"]]

    return version_returned

def get_model_list_pipeline(match_query, offset, limit, order, total_documents, list_name, pagination_path):
    """
    This method generates the pipeline using the parameters up above.
    Parameters:
        match_query (dict): The query to match
        offset (int): The offset to start at
        limit (int): The maximum number of items to return
        order (str): The order in which to sort the results
        total_documents (int): The total number of documents matched with the query
        list_name (str): The name of the list parameter of the (Model)List

    Returns:
        The Pipeline generated
    """

    pipeline = [
        {
            "$match": match_query
        },
        {
            "$sort": {
                "creation_date": -1 if order == "recent" else 1
            }
        },
        {
            "$skip": (offset if offset is not None else 0)
        },
        {
            "$limit": (limit if limit is not None else 20)
        },
        *transform_article_ids_pipeline,
        {
            "$group": {
                "_id": None,
                list_name: {
                    "$push": "$$ROOT"
                }
            }
        },
        {
            "$addFields": {
                "total": total_documents,
                "offset": offset,
                "limit": limit,
                "next": {
                    "$cond": {
                        "if": {"$lt": [offset + limit, total_documents]},
                        "then": f"/{pagination_path}?offset={offset + limit}&limit={limit}&order={order if order else ''}",
                        "else": None
                    }
                },
                "previous": {
                    "$cond": {
                        "if": {"$gt": [offset, 0]},
                        "then": f"/{pagination_path}?offset={max(offset - limit, 0)}&limit={limit}&order={order if order else ''}",
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
    return pipeline


class DefaultArticleAPI(BaseV1PublicApi):

    def __init__(self):
        super().__init__()

    async def get_article_by_id_v1(
            self,
            id: str,
    ) -> ArticleV1:
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_article_ids_pipeline
        ]

        article = await mongodb["article"].aggregate(pipeline).to_list(length=1)

        if not article[0]:
            raise Exception

        article = get_original_article_title(article[0])

        return article

    async def get_article_by_name_v1(
            self,
            name: str,
            wiki_id: str
    ) -> ArticleVersionV1:

        version_id_pipeline = [
            {
                '$match': {
                    "$or": [
                        {"title.en": name},
                        {"title.es": name},
                        {"title.fr": name}
                    ],
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

        version_object_id = await mongodb["article"].aggregate(version_id_pipeline).to_list(length=1)

        if not version_object_id[0]:
            raise Exception

        version_pipeline = [
            {
                '$match': {
                    '_id': version_object_id[0]["_id"],
                }
            },
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(version_pipeline).to_list(length=1)

        if not article_version[0]:
            raise Exception
        article_version = get_original_article_version_title(article_version[0])

        return article_version

    async def get_article_version_by_id_v1(
            self,
            id: str,
    ) -> ArticleVersionV1:
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(pipeline).to_list(length=1)

        if not article_version[0]:
            raise Exception

        article_version = get_original_article_version_title(article_version[0])

        return article_version

    async def get_article_by_author_v1(
            self,
            id: str,
            offset: int,
            limit: int,
            order: str,
    ) -> ArticleListV1:

        total_documents = await get_total_number_of_documents(mongodb["article"],
                                                              {"author._id": ObjectId(id)})

        pipeline = get_model_list_pipeline({"author._id": ObjectId(id)},
                                           offset, limit, order, total_documents, "articles",
                                           "articles/author/")

        articles = await mongodb["article"].aggregate(pipeline).to_list(None)

        if not articles[0]:
            raise Exception

        for article in articles[0]["articles"]:
            get_original_article_title(article)

        return articles[0]

    async def search_articles_v1(
            self,
            wiki_id: str,
            name: str,
            tags: List[str],
            offset: int,
            limit: int,
            order: str,
            creation_date: str,
            author_name: str,
            editor_name: str,
    ) -> ArticleListV1:
        """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
        url_filters = "/articles?"
        matching_variables = {}
        if wiki_id is not None:
            matching_variables["wiki_id"] = ObjectId(wiki_id)
            url_filters += "wiki_id=" + wiki_id + "&"

        if name is not None:
            matching_variables["title"] = {
                "$regex": ".*" + name + ".*",
                "$options": "i"
            }
            url_filters += "name=" + name + "&"

        if tags is not None:
            tag_ids = []
            for tag in tags:
                tag_ids.append(ObjectId(tag))
                url_filters += "tags=" + tag + "&"

            matching_variables["tags._id"] = {"$all": tag_ids}

        if creation_date is not None:
            dates = creation_date.split("-")
            if len(dates) == 1:
                matching_variables["creation_date"] = datetime.strptime(dates[0], "%Y/%m/%d")
            elif len(dates) == 2:
                matching_variables["creation_date"] = {
                    "$gte": datetime.strptime(dates[0], "%Y/%m/%d"),
                    "$lte": datetime.strptime(dates[1], "%Y/%m/%d")
                }

            url_filters += "creation_date=" + creation_date + "&"

        if author_name is not None:
            matching_variables["author.name"] = author_name
            url_filters += "author_name=" + author_name + "&"
        if editor_name is not None:
            matching_variables["versions.author.name"] = editor_name
            url_filters += "editor_name=" + editor_name + "&"

        sorting_variables = {}
        if order is not None:
            if order == "recent":
                sorting_variables["creation_date"] = -1
            elif order == "oldest":
                sorting_variables["creation_date"] = 1
            elif order == "unpopular":
                sorting_variables["rating"] = 1
            else:
                sorting_variables["rating"] = -1

            url_filters += "order=" + order + "&"
        else:
            sorting_variables["rating"] = -1

        total_count = await mongodb['article'].count_documents(matching_variables)

        next_url = (url_filters + "offset=" + str(offset + limit) + "&limit=" + str(limit)) if (
                                                                                                           offset + limit) < total_count else None
        previous_url = (url_filters + "offset=" + str(max(offset - limit, 0)) + "&limit=" + str(
            limit)) if offset > 0 else None

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

        pagination_pipeline = [
            {
                "$addFields": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "next": next_url,
                    "previous": previous_url,
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

        articles = await mongodb["article"].aggregate(query_pipeline).to_list(length=None)

        if not articles:
            raise Exception

        return articles[0]

    async def get_article_version_list_by_article_idv1(
            self,
            id: str,
            offset: int,
            limit: int,
            order: str,
    ) -> ArticleVersionListV1:
        total_documents = await get_total_number_of_documents(mongodb["article_version"],
                                                              {"article_id": ObjectId(id)})

        pipeline = get_model_list_pipeline({"article_id": ObjectId(id)},
                                           offset, limit, order, total_documents, "article_versions",
                                           f"articles/{id}/versions")

        article_versions = await mongodb["article_version"].aggregate(pipeline).to_list(length=None)

        if not article_versions[0]:
            raise Exception

        return article_versions[0]

    async def get_articles_commented_by_user_v1(
            self,
            id: str,
            offset: int,
            limit: int,
            order: str,
    ) -> ArticleListV1:
        comment_list = await get_user_comments(id)
        article_ids_list = []
        for comment in comment_list["comments"]:
            article_ids_list.append(ObjectId(comment["article_id"]))

        total_articles = await get_total_number_of_documents(mongodb["article"],
                                                             {"_id": {"$in": article_ids_list}})

        pipeline = get_model_list_pipeline({"_id": {"$in": article_ids_list}},
                                           offset, limit, order, total_articles, "articles",
                                           f"articles/commented_by/{id}")

        article_list = await mongodb["article"].aggregate(pipeline).to_list(length=None)

        if not article_list[0]:
            raise Exception

        return article_list[0]
