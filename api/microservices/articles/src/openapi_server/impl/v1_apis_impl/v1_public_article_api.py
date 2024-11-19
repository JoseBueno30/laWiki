from datetime import datetime
from typing import List

from bson import ObjectId

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
from openapi_server.impl.utils.api_calls import get_user_comments
from openapi_server.impl.utils.functions import (
    get_original_article_title,
    get_original_article_version_title,
    get_total_number_of_documents, get_model_list_pipeline,
    transform_article_ids_pipeline, transform_version_ids_pipeline, mongodb, get_original_tags)
from openapi_server.models.models_v1.article_list_v1 import ArticleListV1
from openapi_server.models.models_v1.article_v1 import ArticleV1
from openapi_server.models.models_v1.article_version_list_v1 import ArticleVersionListV1
from openapi_server.models.models_v1.article_version_v1 import ArticleVersionV1


class PublicArticleAPIV1(BaseV1PublicApi):

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
        article = get_original_tags(article)

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
        article_version = get_original_tags(article_version)

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
        article_version = get_original_tags(article_version)

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
                                           "v1/articles/author/"+id)

        articles = await mongodb["article"].aggregate(pipeline).to_list(None)

        if not articles[0]:
            raise Exception

        for article in articles[0]["articles"]:
            get_original_article_title(article)
            get_original_tags(article)

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
            # matching_variables["title"] = {
            #     "$regex": ".*" + name + ".*",
            #     "$options": "i"
            # }
            matching_variables["$or"] = [
                {"title." + key: {"$regex": ".*" + name + ".*", "$options": "i"}}
                for key in ["en", "es", "fr"]
            ]
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

        for article in articles[0]["articles"]:
            get_original_article_title(article)
            get_original_tags(article)

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
                                           f"v1/articles/{id}/versions")

        article_versions = await mongodb["article_version"].aggregate(pipeline).to_list(length=None)

        if not article_versions[0]:
            raise Exception

        for article in article_versions[0]["article_versions"]:
            get_original_article_version_title(article)
            get_original_tags(article)

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
                                           f"v1/articles/commented_by/{id}")

        article_list = await mongodb["article"].aggregate(pipeline).to_list(length=None)

        if not article_list[0]:
            raise Exception

        for article in articles_list[0]["article_versions"]:
            get_original_article_version_title(article)
            get_original_tags(article)

        return article_list[0]
