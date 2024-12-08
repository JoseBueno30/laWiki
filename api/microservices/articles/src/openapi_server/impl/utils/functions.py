from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.models.models_v1.simplified_article_version_v1 import SimplifiedArticleVersionV1

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
                        "name": "$$version.author.name",
                        "image": "$$version.author.image",
                    },
                    "lan": "$$version.lan"
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
        #
        if type(version["title"]) is dict: version["title"] = version["title"][article_returned["lan"]]

    return article_returned

def get_original_article_version_title(article):
    version_returned = article
    version_returned["title"] = version_returned["title"][version_returned["lan"]]

    return version_returned

def get_original_tags(article):
    article_returned = article
    for tag in article_returned["tags"]:
        tag["tag"] = tag["tag"][article_returned["lan"]]

    return article_returned



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
                "creation_date": -1 if order == "recent" else 1,
                "modification_date": -1 if order == "recent" else 1,
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

def article_version_to_simplified_article_version(article_version):
    if type(article_version) is not dict:
        simplified_article_version = article_version.to_dict()
    else:
        simplified_article_version = article_version
    #   Deletes the non-necessary attributes
    simplified_article_version.pop("article_id", None)
    simplified_article_version.pop("tags", None)
    simplified_article_version.pop("body", None)

    return simplified_article_version

def parse_title_to_title_dict(article):
    article["title"] = {
        "en" : article["title"],
        "es" : article["title"],
        "fr" : article["title"],
    }
    article["lan"] = "es" # It doesn't care the language because they're going to be the same


mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = mongodb_client.get_database("laWikiV2BD")
