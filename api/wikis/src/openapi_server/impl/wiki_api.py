
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiDB")

# Removes ObjectID fields and converts them to string
def pipeline_remove_id_filter_name(name : str) -> list :
    return [
        {'$match' : {"name" : name}},
        {'$addFields': {"id": {'$toString': '$_id'}}},
        {'$unset': ["_id", "author._id"]}
    ]

class WikiApi(BaseDefaultApi):
    
    async def create_wiki(self, name: str, limit: int, offset: int, new_wiki: NewWiki) -> Wiki:
        result = await mongodb["wiki"].insert_one(new_wiki)
        final_wiki = Wiki(result.inserted_id
                         , name=new_wiki.name
                         , description=new_wiki.description
                         , rating=None
                         , author=new_wiki.author
                         , tags=[])
        return final_wiki
    
    # No va lol
    async def get_one_wiki_by_name(self, name: str) -> Wiki:
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(name))
        return Wiki.from_dict(result)