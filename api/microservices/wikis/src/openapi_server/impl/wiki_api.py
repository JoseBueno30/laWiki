
from typing import Any, Coroutine, List

from bson import ObjectId
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.apis.admins_api_base import BaseAdminsApi
from openapi_server.apis.internal_api_base import BaseInternalApi
from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body import IdTagsBody
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki, Author
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from openapi_server.impl.misc import MESSAGE_NOT_FOUND, MESSAGE_UNEXPECTED, MESSAGE_NOT_FOUND_NESTED

from datetime import datetime

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiDB")

def check_modification_match(result):
    if result.matched_count < 1: # If _id does not lead to a wiki, causes 404
        raise LookupError(MESSAGE_NOT_FOUND.format(resource="Wiki"))

def check_modification(result):
    if result.matched_count < 1: # If _id does not lead to a wiki, causes 404
        raise LookupError(MESSAGE_NOT_FOUND).format(resource="Wiki")
    elif result.modified_count < 1: # If _id leads to wiki, but failed to update, causes 500
        raise Exception(MESSAGE_NOT_FOUND_NESTED)

# Removes ObjectID fields and converts them to string
def pipeline_remove_id_filter_name(name : str = "", id_wiki: str = "") -> list :
    filter = ({"name" : name}) if name else ({"_id" : ObjectId(id_wiki)})
    return [
        {'$match' : filter},
        {'$addFields': {
                "tags": {
                    "$map": {
                        "input": "$tags",
                        "as": "tag",
                        "in": {
                            "id": {"$toString": "$$tag._id"},
                            "name": "$$tag.name"
                        }
                    }
                },
                "author.id": {"$toString": "$author._id"},
                "id": {'$toString': '$_id'}
                }
        },
        {'$unset': ["_id", "author._id"]}
    ]

class WikiApi(BaseDefaultApi):

    def __init__(self):
        super().__init__()

    async def get_wiki(self, id: str) -> Wiki:
        print(1234567890)
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(id_wiki=id)).to_list(length=1)

        if result.__len__() != 1:
            raise LookupError()

        return result[0]

    async def get_one_wiki_by_name(self, name: str) -> Wiki:
        if ObjectId.is_valid(name):
            return await self.get_wiki(name)
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(name)).to_list(length=1)

        if result.__len__() != 1:
            raise LookupError()

        return result[0]

class WikiApiAdmins(BaseAdminsApi):

    def __init__(self):
        super().__init__()
    
    async def create_wiki(self, name: str, limit: int, offset: int, new_wiki: NewWiki) -> Wiki:
        final_wiki = Wiki(id='0'
                         , name=new_wiki.name
                         , description=new_wiki.description
                         , rating=0
                         , author=Author(id='0',name=new_wiki.author)
                         , tags=[]
                         , creation_date=str(datetime.now()))
        idless = final_wiki
        del idless.id
        del idless.author.id
        result = await mongodb["wiki"].insert_one(idless.to_dict())
        final_wiki.id = str(result.inserted_id)
        return final_wiki
    
    async def remove_wiki(self, id: str) -> None:
        result = await mongodb["wiki"].delete_one({"_id" : ObjectId(id)})
        # Gestionar respuesta
    
class WikiApiInternal(BaseInternalApi):

    def __init__(self):
        super().__init__()
    
    async def check_wiki_by_id(self, id: str) -> Coroutine[Any, Any, None]:
        return await mongodb["wiki"].find_one({"_id": ObjectId(id)}, {"_id": 1}) is not None
    
    async def update_rating(self, id: str, id_ratings_body: IdRatingsBody) -> None:
        update_rating_object = [{"_id" : ObjectId(id)},
                                {"$set" : {"rating": id_ratings_body.rating}}]
        result = await mongodb["wiki"].update_one(filter=update_rating_object[0],
                                         update=update_rating_object[1])
        check_modification(result)

    async def assign_wiki_tags(self, id: str, id_tags_body: IdTagsBody) -> None:
        print(id_tags_body)
        print(id_tags_body.to_json())
        uploaded_obj = []
        for obj in id_tags_body.tag_ids:
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
    
    async def unassign_article_tags(self, id: str, ids: List[str]) -> None:
        id_list = []
        for id_str in ids:
            id_list.append(ObjectId(id_str))
        remove_tags_object = [{ "_id" : ObjectId(id) },
    { "$pull": { "tags": { "_id" : {"$in" : id_list }}}}]
        result = await mongodb["wiki"].update_one(filter=remove_tags_object[0],
                                         update=remove_tags_object[1])
        check_modification_match(result)
        
