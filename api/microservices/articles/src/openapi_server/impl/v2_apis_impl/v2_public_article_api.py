from bson import ObjectId
import mwparserfromhell, pypandoc
from typing import List

from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
from openapi_server.impl.utils.api_calls import translate_body_to_lan
from openapi_server.impl.utils.functions import transform_article_ids_pipeline, mongodb, transform_version_ids_pipeline, \
    get_total_number_of_documents, get_model_list_pipeline
from openapi_server.models.models_v2.article_list_v2 import ArticleListV2
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_list_v2 import ArticleVersionListV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.inline_response200_v2 import InlineResponse200V2

class PublicArticleAPIV2(BaseV2PublicApi):

    def __init__(self):
        super().__init__()

    async def get_article_by_id_v2(
        self,
        id: str,
    ) -> ArticleV2:

        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_article_ids_pipeline
        ]

        article = await mongodb["article"].aggregate(pipeline).to_list(length=1)

        if not article[0]:
            raise Exception

        return article[0]

    async def get_article_by_name_v2(
        self,
        name: str,
        wiki: str,
        lan: str
    ) -> ArticleVersionV2:

        match_stage = {"wiki_id": ObjectId(wiki)}

        if not lan:
            match_stage["$or"] = [
                {"title.en": name.strip()},
                {"title.es": name.strip()},
                {"title.fr": name.strip()},
            ]
        else:
            match_stage["title."+lan] = name.strip()

        version_id_pipeline = [
            {
                '$match': match_stage
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

        version_object_id = await mongodb["article"].aggregate(version_id_pipeline).to_list(length=1)

        if not version_object_id[0]:
            raise Exception

        print("Version id encontrado")
        print(version_object_id)

        version_pipeline = [
            {
                '$match': {
                    '_id': version_object_id[0]["_id"],
                }
            },
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(version_pipeline).to_list(length=1)

        print("version encontrado")

        if not article_version[0]:
            raise Exception

        try:
            if lan:
                lang = lan
            else:
                lang = version_id_pipeline[0]["lan"]
                
            body_translation = await mongodb["article_translation"].find_one(
                {"article_version_id": ObjectId(str(version_object_id[0]["_id"])),
                 "lan": lang})
            print("traduccion encontrada")
            if body_translation:
                article_version[0]["body"] = body_translation["body"]
        except:
            print("No hay traduccion")

        return article_version[0]

    async def get_article_version_list_by_article_idv2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleVersionListV2:

        total_documents = await get_total_number_of_documents(mongodb["article_version"],
                                                              {"article_id": ObjectId(id)})

        pipeline = get_model_list_pipeline({"article_id": ObjectId(id)},
                                           offset, limit, order, total_documents, "article_versions",
                                           f"v2/articles/{id}/versions")

        article_versions = await mongodb["article_version"].aggregate(pipeline).to_list(length=None)

        if not article_versions[0]:
            raise Exception

        return article_versions[0]

    async def get_article_version_by_id_v2(
        self,
        id: str,
        lan: str,
    ) -> ArticleVersionV2:
        pipeline = [
            {"$match": {"_id": ObjectId(id)}},
            *transform_version_ids_pipeline
        ]

        article_version = await mongodb["article_version"].aggregate(pipeline).to_list(length=1)

        if article_version is []:
            raise Exception

        body_translation = await mongodb["article_translation"].find_one({"article_version_id": ObjectId(id)})
        if body_translation:
            article_version[0]["body"] = body_translation["body"]

        return article_version[0]

    async def get_article_by_author_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        total_documents = await get_total_number_of_documents(mongodb["article"],
                                                              {"author._id": ObjectId(id)})

        pipeline = get_model_list_pipeline({"author._id": ObjectId(id)},
                                           offset, limit, order, total_documents, "articles",
                                           "v2/articles/author/"+id)

        articles = await mongodb["article"].aggregate(pipeline).to_list(None)

        if not articles[0]:
            raise Exception

        return articles[0]

    async def get_article_version_body_by_idv2(
        self,
        id: str,
        parsed: bool,
        lan: str,
    ) -> InlineResponse200V2:
        if parsed:
            match_stage = {"article_version_id": ObjectId(id)}
            if lan:
                match_stage["lan"] = lan.strip()

            translation = await mongodb["article_translation"].find_one(match_stage)
            response = translation["body"]
        else:
            article_version = await mongodb["article_version"].find_one({"_id": ObjectId(id)})

            body = article_version["body"]
            if lan and lan is not article_version["lan"]:
                body = await translate_body_to_lan(body, lan)

            # response = mwparserfromhell.parse(body)
            #  response = str(response)
            response = body
        return InlineResponse200V2.from_dict({"body": response})

    async def get_articles_commented_by_user_v2(
        self,
        id: str,
        offset: int,
        limit: int,
        order: str,
    ) -> ArticleListV2:
        comment_list = await get_user_comments(id)

        article_ids_list = []
        for comment in comment_list["comments"]:
            article_ids_list.append(ObjectId(comment["article_id"]))

        total_articles = await get_total_number_of_documents(mongodb["article"],
                                                             {"_id": {"$in": article_ids_list}})

        pipeline = get_model_list_pipeline({"_id": {"$in": article_ids_list}},
                                           offset, limit, order, total_articles, "articles",
                                           f"v2/articles/commented_by/{id}")

        article_list = await mongodb["article"].aggregate(pipeline).to_list(length=None)

        if not article_list[0]:
            raise Exception

        return article_list[0]

    async def search_articles_v2(
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
        lan: str
    ) -> ArticleListV2:
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

        if lan is not None:
            matching_variables["lan"] = lan
            url_filters += "lan=" + lan + "&"

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
            articles.append({
                "articles": [],
                "total": 0,
                "offset": offset,
                "limit": limit,
                "next": None,
                "previous": None,
            })

        return articles[0]