
from typing import Any, Coroutine, List

from bson import ObjectId
from pymongo import ReturnDocument
from openapi_server.apis.default_v2_api_base import BaseDefaultV2Api
from openapi_server.apis.admins_v2_api_base import BaseAdminsV2Api
from openapi_server.apis.internal_v2_api_base import BaseInternalV2Api
from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2
from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.tag_v2 import TagV2
from openapi_server.models.wiki_v2 import WikiV2, AuthorV2
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from openapi_server.impl.misc import *
from openapi_server.impl.api_calls import delete_articles_from_wiki
from pymongo.errors import InvalidOperation

from datetime import datetime

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiV2BD")

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

# Removes ObjectID fields and converts them to string
def pipeline_remove_id_filter_name(name : str = "", id_wiki: str = "") -> list :
    filter = ({"name" : name}) if name else ({"_id" : ObjectId(id_wiki)})
    print(filter)
    return [
        {'$match' : filter},
        *partial_pipeline_filter
    ]

def raise_if_not_id(value: str):
    if not ObjectId.is_valid(value):
        raise TypeError("Must be valid ID")

class WikiApi(BaseDefaultV2Api):

    def __init__(self):
        super().__init__()

    async def get_wiki(self, id: str) -> WikiV2:
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(id_wiki=id)).to_list(length=1)
        
        if result.__len__() != 1:
            raise LookupError("Error finding by ID")

        return result

    async def get_wiki_v2(self, id_name: str, lang: str) -> WikiV2:
        print(id_name)
        print(lang)
        if ObjectId.is_valid(id_name):
            result = await self.get_wiki(id_name)
        else:
            print("By name:")
            result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(name=id_name)).to_list(length=1)

        print(result)
        
        if result.__len__() != 1:
            raise LookupError("Error finding")

        result = result[0]

        if lang != result["lang"] and lang is not None:
            print(result["id"])
            translation = await mongodb["wiki_translation"].find_one({"wiki_id" : ObjectId(result["id"]), "lang" : lang})

            print("Translation:" + str(translation))

            if translation is not None:
                result["description"] = translation["description"]


        return result
    
    async def create_wiki_v2(self, new_wiki_v2: NewWikiV2) -> WikiV2:
        final_wiki = WikiV2(id='1'
                         , name=new_wiki_v2.name
                         , description=new_wiki_v2.description
                         , rating=0
                         , author=AuthorV2(id='0',name=new_wiki_v2.author, image="")
                         , tags=[]
                         , creation_date=str(datetime.now())
                         , lang=new_wiki_v2.lang
                         , image=new_wiki_v2.image)
        idless = final_wiki
        del idless.id
        del idless.author.id
        result = await mongodb["wiki"].insert_one(idless.to_dict())
        author_id = ObjectId()
        await mongodb["wiki"].update_one({"_id" : result.inserted_id}, {"$set": {"author._id" : author_id}})
        final_wiki.id = str(result.inserted_id)
        final_wiki.author.id = str(author_id)
        return final_wiki

def conditional_field(name: str, value):
    return {name : value} if value is not None else None

class WikiApiAdmins(BaseAdminsV2Api):

    def __init__(self):
        super().__init__()
    
    
    async def remove_wiki_v2(self, id_name: str) -> None:
        raise_if_not_id(id_name)
        
        delete_articles_from_wiki(id_name)

        result = await mongodb["wiki"].delete_one({"_id" : ObjectId(id_name)})

        if not result.acknowledged:
            raise InvalidOperation()

    async def update_wiki_v2(self, id: str, new_wiki: NewWikiV2) -> WikiV2:
        raise_if_not_id(id)

        print(new_wiki)

        result = await mongodb["wiki"].find_one_and_update({"_id" : ObjectId(id)}
                                            ,
                                            {
                                                "$set": {
                                                    "name" : new_wiki.name,
                                                    "description": new_wiki.description,
                                                    "author.name": new_wiki.author,
                                                    "image": new_wiki.image,
                                                    "lang": new_wiki.lang
                                                }
                                            }
                                            ,upsert=False
                                            ,return_document=ReturnDocument.AFTER)

        print("Documento: " + str(result))

        if result is None:
            raise LookupError("Cannot find wiki")
        
        raise UnicodeError("I can't figure this out, but it does update")
        
        #final_wiki = WikiV2(id=str(result["_id"])
        #                 , name=new_wiki.name
        #                 , description=new_wiki.description
        #                 , rating=result["rating"]
        #                 , author=AuthorV2(id=str(result["author"]["_id"]),name=new_wiki.author, image=result["author"]["image"])
        #                 , tags=result["tags"]
        #                 , creation_date=result["creation_date"]
        #                 , lang=new_wiki.lang
        #                 , image=new_wiki.image)
        #
        #return final_wiki
    
class WikiApiInternal(BaseInternalV2Api):

    def __init__(self):
        super().__init__()
    
    async def check_wiki_by_idv2(self, id_name: str) -> None:
        if ObjectId.is_valid(id_name):
            return await mongodb["wiki"].find_one({"_id": ObjectId(id_name)}, {"_id": 1}) is not None
        else:
            return await mongodb["wiki"].find_one({"name": id_name}, {"_id": 1}) is not None
    
    async def update_rating_v2(self, id: str, id_ratings_body: IdRatingsBody) -> None:
        update_rating_object = [{"_id" : ObjectId(id)},
                                {"$set" : {"rating": id_ratings_body.rating}}]
        result = await mongodb["wiki"].update_one(filter=update_rating_object[0],
                                         update=update_rating_object[1])
        check_modification_match(result)

    async def assign_wiki_tags_v2(self, id: str, id_tags_body_v2: IdTagsBodyV2) -> None:
        print(id_tags_body_v2)
        print(id_tags_body_v2.to_json())
        uploaded_obj = []
        for obj in id_tags_body_v2.tag_ids:
            uploaded_obj.append({
            "_id" : ObjectId(obj.id),
            "name" : obj.tag
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
    
    async def unassign_wiki_tags_v2(self, id: str, ids: List[str]) -> None:
        id_list = []
        for id_str in ids:
            id_list.append(ObjectId(id_str))
        remove_tags_object = [{ "_id" : ObjectId(id) },
    { "$pull": { "tags": { "_id" : {"$in" : id_list }}}}]
        result = await mongodb["wiki"].update_one(filter=remove_tags_object[0],
                                         update=remove_tags_object[1])
        check_modification_match(result)
        
