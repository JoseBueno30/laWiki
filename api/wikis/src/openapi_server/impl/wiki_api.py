
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki, Author
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = client.get_database("laWikiDB")

# Removes ObjectID fields and converts them to string
def pipeline_remove_id_filter_name(name : str) -> list :
    return [
        {'$match' : {"name" : name}},
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
    
    async def create_wiki(self, name: str, limit: int, offset: int, new_wiki: NewWiki) -> Wiki:
        final_wiki = Wiki(id='0'
                         , name=new_wiki.name
                         , description=new_wiki.description
                         , rating=0
                         , author=Author(id='0',name=new_wiki.author)
                         , tags=[])
        result = await mongodb["wiki"].insert_one(final_wiki.to_dict())
        final_wiki.id = result.inserted_id
        return final_wiki
    

    async def get_one_wiki_by_name(self, name: str) -> Wiki:
        result = await mongodb["wiki"].aggregate(pipeline_remove_id_filter_name(name)).to_list(length=1)

        if result.__len__() != 1:
            raise LookupError()
        
        print(result)
        print(type(result[0]))

        return result[0]