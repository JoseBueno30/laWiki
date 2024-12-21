from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from openapi_server.apis.v1_internal_api_base import BaseV1InternalApi
from openapi_server.models.new_rating import NewRating
from openapi_server.models.user_info import UserInfo

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")

pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'}}
     },
    {'$unset': ["_id"]}  # Remove the original _id field
]


class V1InternalAPI(BaseV1InternalApi):

    async def check_user(
            self,
            user_id: str,
    ) -> None:
        """Checks wheter the user email is registered in the application"""
        user = await mongodb['user'].find_one({"id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return None

    async def put_user_rating(
            self,
            user_id: str,
            new_rating: NewRating,
    ) -> UserInfo:
        """Update the given user's rating"""
        user = await mongodb['user'].aggregate([*pipeline_remove_id, {'$match': {'id': ObjectId(user_id)}}]).to_list(
            length=None)
        if not user[0]:
            raise HTTPException(status_code=404, detail="User not found")

        await mongodb['user'].update_one({"id": ObjectId(user_id)}, {"$set": {"rating": new_rating.rating}})
        return UserInfo(**{**user[0], "rating": new_rating.rating})
