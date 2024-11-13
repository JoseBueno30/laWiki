import datetime

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.author import Author
from openapi_server.models.average_rating import AverageRating
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from datetime import date
import requests


class RatingsManager (BaseDefaultApi):
    app: FastAPI = FastAPI()
    mongodb_client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
    mongodb = mongodb_client.get_database("laWikiDB")
    wiki_url = "http://wikis_api:8084/"
    article_url = "http://articles_api:8081/"

    async def get_rating(self, id: str):
        pipe = [{'$match': {'_id': self._convert_id_into_ObjectId(id)}},
                {'$addFields': {
                    'id': {'$toString': '$_id'},
                    'article_id': {'$toString': '$article_id'},
                    'author': {'id': {'$toString': '$author._id'}}}},
                {'$unset': '_id'},
                {'$unset': 'author._id'}]
        result = await self._check_rating_exists(id, pipe)
        return result;

    async def delete_rating(self, id: str):
        result = await self.mongodb["rating"].delete_one({'_id': self._convert_id_into_ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Rating Not Found")
        await self._update_article_and_wiki_average(id)
        return None;

    async def rate_article(self, id: str, new_rating: NewRating):
        self._check_new_rating_is_valid(new_rating)
        article = await self._check_article_exists(id)
        await self._check_user_has_no_rating(id, new_rating.author_id)

        # Check if author exists
        # TODO: No users in the database yet

        rating = {
            "article_id": self._convert_id_into_ObjectId(id),
            "value": new_rating.value,
            "creation_date": datetime.datetime.now(),
            "author": {
                # TODO: No users in the database yet
                "_id": self._convert_id_into_ObjectId(new_rating.author_id),
                "name": "Author Name",
                "image": "default_image_url"
            },
        }
        result = await self.mongodb["rating"].insert_one(rating);
        await self._update_article_and_wiki_average(id)
        # Change the ObjectId value to string
        rating['id'] = str(result.inserted_id);
        rating['creation_date'] = date.today();
        rating['article_id'] = id;
        rating['author']['id'] = new_rating.author_id;

        return rating;

    async def edit_article_rating(self, id: str, rating: Rating):
        self._check_new_rating_is_valid(rating)
        article = await self._check_article_exists(id)
        result = await self._check_rating_exists(rating.id)

        result['value'] = rating.value
        await self.mongodb["rating"].update_one({'_id': self._convert_id_into_ObjectId(rating.id)}, {'$set': result})
        await self._update_article_and_wiki_average(id)
        return rating;

    async def get_article_average_rating(self, id: str):
        await self._check_article_exists(id)

        result = await self.mongodb["rating"].find({'article_id': self._convert_id_into_ObjectId(id)}).to_list(length=None)
        if result == None or len(result) == 0:
            raise HTTPException(status_code=404, detail="No Ratings found with that article ID")

        avgRating = AverageRating(total=0, five_count=0, four_count=0, three_count=0, two_count=0, one_count=0, average=0.0, total_sum=0)
        avgRating.total = len(result)
        for item in result:
            if item['value'] == 5:
                avgRating.five_count += 1
            elif item['value'] == 4:
                avgRating.four_count += 1
            elif item['value'] == 3:
                avgRating.three_count += 1
            elif item['value'] == 2:
                avgRating.two_count += 1
            elif item['value'] == 1:
                avgRating.one_count += 1
        avgRating.total_sum = 5 * avgRating.five_count + 4 * avgRating.four_count + 3 * avgRating.three_count + 2 * avgRating.two_count + avgRating.one_count
        avgRating.average = avgRating.total_sum / avgRating.total

        return avgRating;

    async def get_ratings_wikis_id(self, id: str):
        wiki = await self._check_wiki_exists(id);
        return wiki.get("rating");

    async def get_ratings_articles_id_users_id(self,articleId: str,userId: str,):
        await self._check_article_exists(articleId)
        # user = await self.mongodb["users"].find_one({'_id': self._convert_id_into_ObjectId(userId)})
        pipe = [
                {'$match': {
                    'article_id': self._convert_id_into_ObjectId(articleId),
                    'author._id': self._convert_id_into_ObjectId(userId)

                }},
                {'$addFields': {
                    'id': {'$toString': '$_id'},
                    'article_id': {'$toString': '$article_id'},
                    'author.id': {'$toString': '$author._id'}
                }},
                {'$unset': ['_id', 'author._id']}
            ]
        result = await self.mongodb["rating"].aggregate(pipe).to_list(length=1)
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Rating Not Found")
        return result[0]

    async def get_user_rating(self, id: str):
        # TODO: No users in the database yet
        return 0.0;

    ##-----------------------------------------------------------------------------------------------------------------
    ##--------------------------------------Private Methods------------------------------------------------------------
    ##-----------------------------------------------------------------------------------------------------------------
    async def _check_article_exists(self, id: str):
        # article = await self.mongodb["article"].find_one({'_id': self._convert_id_into_ObjectId(id)})
        # if article == None:
        #     raise HTTPException(status_code=404, detail="Article Not Found")
        # return article;

        try:
            response = requests.head(self.article_url + "articles/" + id)
            response.raise_for_status()  # Verifica si hubo un error HTTP
            return response  # Retorna el JSON si la respuesta es exitosa
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail="Error connecting to the articles service")

    async def _check_rating_exists(self, id: str = 0, pipe: list = []):
        if pipe == []:
            pipe = [{'$match': {'_id': self._convert_id_into_ObjectId(id)}}]
        result = await self.mongodb["rating"].aggregate(pipe).to_list(length=1)
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Rating Not Found")
        return result[0]

    async def _check_wiki_exists(self, id: str):
        wiki = await self.mongodb["wiki"].find_one({'_id': self._convert_id_into_ObjectId(id)})
        if wiki == None:
            raise HTTPException(status_code=404, detail="Wiki Not Found")
        return wiki;

    def _check_new_rating_is_valid(self, new_rating: NewRating or Rating):
        author_id = new_rating.author_id if isinstance(new_rating, NewRating) else new_rating.author.id
        if new_rating is None or new_rating.value is None or new_rating.value < 0 or new_rating.value > 5 or author_id is None:
            raise HTTPException(status_code=400, detail="Invalid Rating")
        return None;

    async def _update_article_and_wiki_average(self, id):
        article_rating = await self.get_article_average_rating(id)
        newAvg = article_rating.average
        article = None;
        article_list = None;

        try:
            updateArticle = requests.put(self.article_url + "articles/" + id +"/ratings", json = {'rating': newAvg })
            updateArticle.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=updateArticle.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail="Error connecting to the articles service on update article's rating")

        try:
            article = requests.get(self.article_url + "articles/" + id)
            article.raise_for_status()
            article = article.json()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=article.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail="Error connecting to the articles service on getting the article")
        try:

            article_list = requests.get(self.article_url + "articles?wiki_id=" + article['wiki_id'])
            article_list.raise_for_status()
            article_list = article_list.json()

        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=article_list.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail="Error connecting to the articles on getting the article list")

        try:
            total = 0;
            for articles in article_list['articles']:
                total += articles['rating']
            update_wiki = requests.put(self.wiki_url + "wikis/" + article['wiki_id'] + "/ratings", json={'rating': total / len(article_list['articles']) })
            update_wiki.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=updateArticle.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail="Error connecting to the wiki service")

    async def _check_user_has_no_rating(self, id: str, author_id: str):
        result = await self.mongodb["rating"].find({'article_id': self._convert_id_into_ObjectId(id), 'author._id': self._convert_id_into_ObjectId(author_id)}).to_list(length=None)
        if len(result) > 0:
            raise HTTPException(status_code=422, detail="You have already rated this article")
        return None;

    def _convert_id_into_ObjectId(self, id: str):
        try:
            return ObjectId(id)
        except:
            raise HTTPException(status_code=404, detail="Invalid ID format")
