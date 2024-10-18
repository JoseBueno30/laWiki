from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from contextlib import asynccontextmanager# place these at the top of your .py file

# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)

# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
    app.mongodb = app.mongodb_client.get_database("laWikiDB")
    print("MongoDB connected.")

# method to close the database connection
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")


app: FastAPI = FastAPI(lifespan=lifespan)

# Crear una ruta GET para la raíz del servidor
@app.get("/")
def read_root():
    return {"message": "Welcome to LaWiki!"}

# Obtiene todos los artículos
@app.get("/articles")
async def read_article():
    articles = await app.mongodb["article"].find().to_list(None)
    print(articles)
    return articles

# Obtiene todos los artículos
@app.get("/wikis")
async def read_article():
    return await app.mongodb["wiki"].find().to_list()

# uvicorn main:app --reload