import re
from typing import Any, Coroutine, List, Dict
from pydantic import StrictStr, StrictBool

from bson import ObjectId
from pymongo import ReturnDocument
from openapi_server.apis.default_v3_api_base import BaseDefaultV3Api
from openapi_server.apis.admins_v3_api_base import BaseAdminsV3Api
from openapi_server.apis.internal_v3_api_base import BaseInternalV3Api
from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2
from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.tag_v2 import TagV2
from openapi_server.models.wiki_list_v2 import WikiListV2
from openapi_server.models.wiki_v2 import WikiV2, AuthorV2
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.exceptions import RequestValidationError
from openapi_server.impl.misc import *
from openapi_server.impl.api_calls import delete_articles_from_wiki, translate_body_to_lan, translate_text_to_lan, delete_tags_from_wiki, get_user_by_id
from pymongo.errors import InvalidOperation

from datetime import datetime, timedelta

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiV2BD")
    
async def check_wiki_has_author_equals_user(wiki_author: str, wiki_id: str, admin: bool):
    author_result = None
    if not admin:
        author_result = await mongodb["wiki"].find_one({"_id": ObjectId(wiki_id)}, {"author":
                                                                                    {"$toString": "$author._id"}})
        if author_result["author"] != wiki_author:
            raise RequestValidationError("User is not the author of the wiki")
    return author_result

def check_modification_match(result):
    if result.matched_count < 1: # If _id does not lead to a wiki, causes 404
        raise LookupError(MESSAGE_NOT_FOUND.format(resource="Wiki"))

def check_modification(result):
    if result.matched_count < 1: # If _id does not lead to a wiki, causes 404
        raise LookupError(MESSAGE_NOT_FOUND.format(resource="Wiki"))
    elif result.modified_count < 1: # If _id leads to wiki, but failed to update, causes 500
        raise Exception(MESSAGE_NOT_FOUND_NESTED)

partial_pipeline_filter = [{'$addFields': {
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
                "author.id": {"$toString": "$author._id"},
                "id": {'$toString': '$_id'}
                }
        },
        {'$unset': ["_id", "author._id"]}]

move_name_filter = [{'$addFields': {
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
                "author.id": {"$toString": "$author._id"},
                "id": {'$toString': '$_id'}
                }
        },
        {
            "$project": {
                "name": { "$getField": { "field": "$lang", "input": "$name" } },
                "id": 1,
                "lang": 1,
                "author": 1,
                "rating": 1,
                "tags": 1,
                "description": 1,
                "creation_date": 1,
                "image": 1
            }
        },
        {'$unset': ["_id", "author._id"]}]

def pipepline_remove_id_auto(id_name: str):
        if ObjectId.is_valid(id_name):
            return pipeline_remove_id_filter_name(id_wiki=id_name)
        else:
            return pipeline_remove_id_filter_name(name=id_name)

def match_by_name_or_id(name : str = "", id_wiki : str = ""):
    return {"$expr": {
        "$or" : [
            {"$eq": [
                        { "$getField": { "field": "es", "input": "$name" } }, name
                    ]},
                    {"$eq": [
                        { "$getField": { "field": "fr", "input": "$name" } }, name
                    ]},
                    {"$eq": [
                        { "$getField": { "field": "en", "input": "$name" } }, name
                    ]}
            ]}} if name else ({"_id" : ObjectId(id_wiki)})

# Removes ObjectID fields and converts them to string
def pipeline_remove_id_filter_name(name : str = "", id_wiki: str = "") -> list :
    filter = match_by_name_or_id(name,id_wiki)
    print(filter)
    return [
        {'$match' : filter},
        *partial_pipeline_filter
    ]

def raise_if_not_id(value: str):
    if not ObjectId.is_valid(value):
        raise TypeError("Must be valid ID")


async def translate_wiki(languages : List[str], wiki_lang: str, name: Dict[str, str], description: str, target_wiki: ObjectId):
    """Translates and uploads all necessary translations, name should be translated already"""
    for lang in [x for x in languages if x != wiki_lang]:
        translation = {}
        translation["wiki_id"] = target_wiki
        translation["description"] = await translate_text_to_lan(description, lang)
        translation["lang"] = lang
        translation["name"] = name[lang]
        upd_result = await mongodb["wiki_translation"].replace_one({"wiki_id" : target_wiki, "lang" : lang}, translation,upsert=True)
    translation = {}
    translation["wiki_id"] = target_wiki
    translation["description"] = description
    translation["lang"] = wiki_lang
    translation["name"] = name[wiki_lang]
    upd_result = await mongodb["wiki_translation"].replace_one({"wiki_id" : target_wiki, "lang" : wiki_lang}, translation,upsert=True)
    

async def translate_name(wiki: NewWikiV2):
    if wiki.translate:
        name = {}
        name[wiki.lang] = wiki.name
        for lang in [x for x in SUPPORTED_LANGUAGES if x != wiki.lang]:
            name[lang] = await translate_text_to_lan(wiki.name,lang)
    else:
        name = {}
        name["es"] = wiki.name
        name["en"] = wiki.name
        name["fr"] = wiki.name
    print(name)
    return name

def discriminate_name(name: str):
    if ObjectId.is_valid(name):
        raise InvalidOperation("Name cannot be a valid 12-byte integer.")
    
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 ]+$'
    if not bool(re.match(pattern, name)):
        raise InvalidOperation("Name cannot contain special characters, such as \"_\". Only alphanumeric characters, and ñ, are allowed, they may be accented.")

class WikiApi(BaseDefaultV3Api):

    def __init__(self):
        super().__init__()

    async def get_wiki(self, id: str) -> WikiV2:
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(id_wiki=id)).to_list(length=1)
        
        if result.__len__() != 1:
            raise LookupError("No wiki found by ID")

        return result

    async def get_wiki_v3(self, id_name: str, lang: str) -> WikiV2:
        print(id_name)
        print(lang)
        print("By name:")
        result = await mongodb["wiki"].aggregate(pipepline_remove_id_auto(id_name)).to_list(length=1)

        print(result)
        
        if result.__len__() != 1:
            raise LookupError("No wiki found")

        result = result[0]

        if lang != result["lang"] and lang is not None:
            print(result["id"])
            translation = await mongodb["wiki_translation"].find_one({"wiki_id" : ObjectId(result["id"]), "lang" : lang})

            print("Translation:" + str(translation))

            if translation is not None:
                result["name"][lang] = translation["name"]
                result["description"] = translation["description"]


        return result
    
    async def create_wiki_v3(self, user_id: StrictStr, admin: StrictBool, new_wiki_v2: NewWikiV2) -> WikiV2:
        
        user = get_user_by_id(user_id)

        discriminate_name(new_wiki_v2.name)

        try:
            name = await translate_name(new_wiki_v2)
        except Exception as e:
            print(e)
            raise ConnectionError("Cannot connect to translator")

        final_wiki = WikiV2(id='1'
                         , name=name
                         , description=new_wiki_v2.description
                         , rating=0
                         , author=AuthorV2(id=user["id"],name=user["username"], image=user["image"])
                         , tags=[]
                         , creation_date=str(datetime.now())
                         , lang=new_wiki_v2.lang
                         , image=new_wiki_v2.image)
        idless = final_wiki.model_dump()
        idless.pop("id")
        idless["author"].pop("id")
        idless["author"]["_id"] = ObjectId(user_id)
        print(idless)
        result = await mongodb["wiki"].insert_one(idless)
        final_wiki.id = str(result.inserted_id)

        await translate_wiki(SUPPORTED_LANGUAGES, new_wiki_v2.lang, name, new_wiki_v2.description, result.inserted_id)

        return final_wiki

    async def search_wikis_v3(self, name: str, offset: int, limit: int, order: str, creation_date: str, author_name: str, lang: str) -> WikiListV2:
        filters = {}
        url_filters = "/wikis?"

        if author_name is not None:
            filters["author.name"] = author_name
            url_filters += "author_name=" + author_name + "&"

        if name is not None:
            filters["$or"] = [
                {"name." + key: {"$regex": ".*" + name + ".*", "$options": "i"}}
                for key in SUPPORTED_LANGUAGES
            ]
            url_filters += "name=" + name + "&"

        if creation_date is not None:
            dates = creation_date.split("-")
            if len(dates) == 1:
                filters["creation_date"] = { #Todo el día elegido
                    "$gte": (datetime.strptime(dates[0] , "%Y/%m/%d")),
                    "$lt": (datetime.strptime(dates[0] , "%Y/%m/%d") + timedelta(1))
                }
            elif len(dates) == 2:
                filters["creation_date"] = {
                    "$gte": (datetime.strptime(dates[0] , "%Y/%m/%d")),
                    "$lte": (datetime.strptime(dates[1] , "%Y/%m/%d"))
                }

            url_filters += "creation_date=" + creation_date + "&"
        
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

        total_count = await mongodb['wiki'].count_documents(filters)

        next_url = (url_filters + 
                    "offset=" + str(offset + limit) + 
                    "&limit=" + str(limit)) if (offset + limit) < total_count else None
        previous_url = (url_filters + "offset=" + str(max(offset - limit, 0)) + 
                        "&limit=" + str(limit)) if offset > 0 else None
        
        #if lang is not None:
        #    url_filters += "lang=" + lang + "&"

        # https://www.google.com/search?q=paging+meaning
        paging_pipeline = [
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

        group_articles_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "wikis": {
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

        query_pipeline = [
            {"$match": filters},
            {"$sort": sorting_variables},
            {"$skip": offset},
            {"$limit": limit},
            *move_name_filter,
            *group_articles_pipeline,
            *paging_pipeline
        ]

        wikis = await mongodb["wiki"].aggregate(query_pipeline).to_list(length=None)

        print(query_pipeline, end="\n\n")
        #print(wikis[0]["wikis"])

        if not wikis:
            return {"wikis": [],
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "next": next_url,
                    "previous": previous_url
            }

        if lang is not None:
            ids = list(map(lambda x: ObjectId(x["id"]),wikis[0]["wikis"]))
            print(ids)
            try:
                traducciones = await mongodb["wiki_translation"].find({"wiki_id" : {"$in" : ids}, "lang" : lang}, {"wiki_id" : {"$toString" : "$wiki_id"}, "description" : 1, "name" : 1, "_id" : 0}).to_list(length=None)
            except:
                print("Error buscando traducciones")
            
            print("Diferencia: " + str(len(traducciones) - len(wikis[0]["wikis"])))
            wiki_ids = list(map(lambda x: x["wiki_id"],traducciones))
            print(wiki_ids)
            for wiki in wikis[0]["wikis"]:
                try:
                    i = wiki_ids.index(wiki["id"])
                    wiki["description"] = traducciones[i]["description"]
                    wiki["name"] = traducciones[i]["name"]
                except:
                    print("Sin traduccion:" + wiki["id"] + ", " + wiki["name"])
                    pass

        return wikis[0]

def poner_traduccion(dato: dict, traduccion: dict):
    resultado = dato.copy()
    resultado["description"] = traduccion["description"]
    resultado["name"] = traduccion["name"]
    return resultado

def conditional_field(name: str, value):
    return {name : value} if value is not None else None

async def delete_translations(wiki_id):
    await mongodb["wiki_translation"].delete_many({"wiki_id" : ObjectId(wiki_id)})

async def get_id(name: str):
    result = await mongodb["wiki"].find_one(match_by_name_or_id(name,""),{"_id" : 0, "id" : {"$toString" :"$_id"}})
    return result["id"]

class WikiApiAdmins(BaseAdminsV3Api):

    def __init__(self):
        super().__init__()
    
    
    async def remove_wiki_v3(self, user_id: StrictStr, admin: StrictBool, id_name: str) -> None:
        if not ObjectId.is_valid(id_name): # Si es nombre se cambia por id
            id_name = await get_id(id_name)
        
        await check_wiki_has_author_equals_user(user_id, id_name, admin)
        
        delete_articles_from_wiki(id_name)

        delete_tags_from_wiki(id_name)

        await delete_translations(id_name)

        result = await mongodb["wiki"].delete_one({"_id" : ObjectId(id_name)})

        if not result.acknowledged:
            raise InvalidOperation()

    async def update_wiki_v3(self, user_id: StrictStr, admin: StrictBool, id: str, new_wiki: NewWikiV2) -> WikiV2:
        if ObjectId.is_valid(id):
            name = ""
        else:
            name = id

        await check_wiki_has_author_equals_user(user_id, id, admin)

        user = get_user_by_id(user_id)
        
        discriminate_name(new_wiki.name)

        new_wiki_dict = new_wiki.to_dict()
        
        translated_name = await translate_name(new_wiki)

        new_wiki_dict["name"] = translated_name

        result = await mongodb["wiki"].find_one_and_update(match_by_name_or_id(name,id)
                                            ,
                                            {
                                                "$set": {
                                                    "name" : translated_name,
                                                    "description": new_wiki.description,
                                                    "author.name": user["username"],
                                                    "author.image": user["image"],
                                                    "author._id": ObjectId(user["id"]),
                                                    "image": new_wiki.image,
                                                    "lang": new_wiki.lang
                                                }
                                            }
                                            ,upsert=False
                                            ,return_document=ReturnDocument.AFTER)

        if result is None:
            raise LookupError("Cannot find wiki")
        
        try:
            await translate_wiki(SUPPORTED_LANGUAGES, result["lang"], translated_name, new_wiki.description, result["_id"])
        except Exception as e:
            print(e)
            raise ConnectionError("Cannot connect to translator")

        new_wiki_dict.pop("translate")
        new_wiki_dict["id"] = str(result["_id"])
        result["author"]["id"] = str(result["author"].pop("_id"))
        new_wiki_dict["author"] = result["author"]

        new_wiki_dict["tags"] = []
        for tag in result["tags"]:
            tag["id"] = str(tag.pop("_id"))
            new_wiki_dict["tags"].append(tag)

        new_wiki_dict["rating"] = result["rating"]
        new_wiki_dict["creation_date"] = result["creation_date"]
        new_wiki_dict["author"] = result["author"]

        print(new_wiki_dict)
        final_wiki = WikiV2.from_dict(new_wiki_dict)
        print(final_wiki)
        
        return final_wiki
    
class WikiApiInternal(BaseInternalV3Api):

    def __init__(self):
        super().__init__()
    
    async def check_wiki_by_idv3(self, id_name: str) -> None:
        if ObjectId.is_valid(id_name):
            return await mongodb["wiki"].find_one({"_id": ObjectId(id_name)}, {"_id": 1}) is not None
        else:
            return await mongodb["wiki"].find_one({"name": id_name}, {"_id": 1}) is not None
    
    async def update_rating_v3(self, user_id: StrictStr, admin: StrictBool, id: str, id_ratings_body: IdRatingsBody) -> None:
        update_rating_object = [{"_id" : ObjectId(id)},
                                {"$set" : {"rating": id_ratings_body.rating}}]
        result = await mongodb["wiki"].update_one(filter=update_rating_object[0],
                                         update=update_rating_object[1])
        check_modification_match(result)

    async def assign_wiki_tags_v3(self, id: str, user_id: StrictStr, admin: StrictBool, id_tags_body_v2: IdTagsBodyV2) -> None:
        await check_wiki_has_author_equals_user(user_id, id, admin)

        print(id_tags_body_v2)
        print(id_tags_body_v2.to_json())
        uploaded_obj = []
        for obj in id_tags_body_v2.tag_ids:
            uploaded_obj.append({
            "_id" : ObjectId(obj.id),
            "tag" : obj.tag
        })
        add_tags_object = [
            { "_id" : ObjectId(id) }
            ,
            {
                "$addToSet" : {
                    "tags" : {
                        "$each": uploaded_obj
                    }
                }
            }
            ]
        result = await mongodb["wiki"].update_one(filter=add_tags_object[0],
                                         update=add_tags_object[1])
        check_modification_match(result) 
    
    async def unassign_wiki_tags_v3(self, id: str, user_id: StrictStr, admin: StrictBool, ids: List[str]) -> None:
        await check_wiki_has_author_equals_user(user_id, id, admin)

        id_list = []
        for id_str in ids:
            id_list.append(ObjectId(id_str))
        remove_tags_object = [{ "_id" : ObjectId(id) },
    { "$pull": { "tags": { "_id" : {"$in" : id_list }}}}]
        result = await mongodb["wiki"].update_one(filter=remove_tags_object[0],
                                         update=remove_tags_object[1])
        check_modification_match(result)
        
