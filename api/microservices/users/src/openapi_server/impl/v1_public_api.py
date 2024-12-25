from fastapi import HTTPException

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
from openapi_server.models.new_user_info import NewUserInfo
from openapi_server.models.public_user_info import PublicUserInfo
from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse
from firebase_admin import auth
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")

pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'}}},
    {'$unset': ["_id"]}  # Remove the original _id field
]


def validate_user(user, user_email, admin):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user[0]["email"], user_email, admin)
    if user[0]["email"] != user_email and not admin:
        raise HTTPException(status_code=401, detail="User unauthorized for this operation")


class V1PublicAPI(BaseV1PublicApi):

    async def get_user_info(
            self,
            user_id: str,
    ) -> PublicUserInfo:
        """Get user information"""
        user = await mongodb['user'].aggregate([
            {"$match": {"_id": ObjectId(user_id)}}, *pipeline_remove_id]).to_list(length=None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return PublicUserInfo(**{**user[0], "admin" : None})
