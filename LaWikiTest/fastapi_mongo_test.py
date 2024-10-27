from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app: FastAPI = FastAPI()

mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

mongodb = mongodb_client.get_database("laWikiDB")

# removes _id field for new id field, returns _id as string
pipeline_remove_id = [{'$addFields': { "id" : { '$toString' : '$_id'}}}, {'$unset' : ["_id"]}]

# Create a GET route for the server root
@app.get("/")
def read_root():
    return {"message": "Welcome to LaWiki!"}

# Get all articles
@app.get("/articles")
async def read_article():
    #pull multiple records from DB with serialized ObjectId
    articles = await mongodb["article"].aggregate(pipeline_remove_id).to_list()
    print(articles)
    return articles

# Get all comments
@app.get("/comments")
async def read_article():
    comments = await mongodb["comment"].aggregate(pipeline_remove_id).to_list()
    print(comments)
    return comments
