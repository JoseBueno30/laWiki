from fastapi import HTTPException

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
from openapi_server.models.new_user_info import NewUserInfo
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
            user_email: str,
            admin: bool,
    ) -> UserInfo:
        """Retrieves user info by the unique user id"""
        user_info = await mongodb['user'].aggregate(
            [{'$match': {'_id': ObjectId(user_id)}}, *pipeline_remove_id]
        ).to_list(length=None)
        validate_user(user_info, user_email, admin)

        return UserInfo(**user_info[0])

    async def post_verify_token(
            self,
            auth_token: str,
    ) -> VerifyResponse:
        """Returns user info from the user oatuh token"""
        try:
            decoded_token = auth.verify_id_token(auth_token)
            token_email = decoded_token['email']
            token_username = decoded_token['name']
            token_image = decoded_token['picture']
            token_iat = decoded_token['iat']
            token_exp = decoded_token['exp']
        except Exception as e:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")

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

        return VerifyResponse(auth_token=auth_token, iat_date=token_iat, exp_date=token_exp, user_info=user_info)

    async def put_user_info(self, user_id: str, user_email: str, admin: bool, new_user_info: NewUserInfo) -> UserInfo:
        """Updates user account info"""
        user = await mongodb['user'].aggregate(
            [{'$match': {'_id': ObjectId(user_id)}}, *pipeline_remove_id]
        ).to_list(length=None)
        validate_user(user, user_email, admin)
        updated_fields = {
            "username": new_user_info.username,
            "image": new_user_info.image
        }
        await mongodb['user'].update_one({'_id': ObjectId(user_id)}, {'$set': updated_fields})
        return UserInfo(**{**user[0], **updated_fields})

    async def put_user_image(self, user_id: str, user_email: str, admin: bool, body: str) -> UserInfo:
        """Update the given user's profile picture"""
        user = await mongodb['user'].aggregate(
            [{'$match': {'_id': ObjectId(user_id)}}, *pipeline_remove_id]
        ).to_list(length=None)

        validate_user(user, user_email, admin)
        await mongodb['user'].update_one({'_id': ObjectId(user_id)}, {'$set': {"image": body}})
        return UserInfo(**{**user[0], "image": body})

    async def put_user_username(self, user_id: str, user_email: str, admin: bool, body: str) -> UserInfo:
        """Update the given user's username"""
        user = await mongodb['user'].aggregate(
            [{'$match': {'_id': ObjectId(user_id)}}, *pipeline_remove_id]
        ).to_list(length=None)

        validate_user(user, user_email, admin)
        await mongodb['user'].update_one({'_id': ObjectId(user_id)}, {'$set': {"username": body}})
        return UserInfo(**{**user[0], "username": body})
