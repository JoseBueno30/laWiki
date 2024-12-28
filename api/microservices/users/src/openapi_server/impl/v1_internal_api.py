from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from firebase_admin import auth

from openapi_server.apis.v1_internal_api_base import BaseV1InternalApi
from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse

client = AsyncIOMotorClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")
mongodb = client.get_database("laWikiV2BD")

pipeline_remove_id = [
    {'$addFields': {"id": {'$toString': '$_id'}}
     },
    {'$unset': ["_id"]}  # Remove the original _id field
]


class V1InternalAPI(BaseV1InternalApi):

    async def put_verify_token(
        self,
        body: str,
    ) -> VerifyResponse:
        """Returns user info from the user oatuh token"""
        try:
            decoded_token = auth.verify_id_token(body)
            token_email = decoded_token['email']
            token_username = decoded_token['name']
            token_image = decoded_token['picture']
            token_iat = decoded_token['iat']
            token_exp = decoded_token['exp']
        except Exception as e:
            raise HTTPException(status_code=401, detail="Unauthorized, invalid token")

        user_info = await mongodb['user'].aggregate(
            [{'$match': {'email': token_email}}, *pipeline_remove_id]
        ).to_list(length=None)
        if user_info:
            user_info = UserInfo(**user_info[0])
        else:
            new_user = {
                'email': token_email,
                'username': token_username,
                'image': token_image,
                'rating': 0,
                'admin': False
            }
            res = await mongodb['user'].insert_one(new_user)
            user_info = UserInfo(**{**new_user, 'id': str(res.inserted_id)})

        return VerifyResponse(auth_token=body, iat_date=token_iat, exp_date=token_exp, user_info=user_info)

    async def put_user_rating(
        self,
        user_id: str,
        body: float,
    ) -> UserInfo:
        """Update the given user's rating"""
        user = await mongodb['user'].aggregate(
            [{'$match': {'_id': ObjectId(user_id)}}, *pipeline_remove_id]
        ).to_list(length=None)
        if not user[0]:
            raise HTTPException(status_code=404, detail="User not found")

        await mongodb['user'].update_one({"_id": ObjectId(user_id)}, {"$set": {"rating": body}})
        return UserInfo(**{**user[0], "rating": body})
