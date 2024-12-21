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
    {'$addFields': {"id": {'$toString': '$_id'}}
     },
    {'$unset': ["_id"]}  # Remove the original _id field
]


class V1PublicAPI(BaseV1PublicApi):

    async def get_user_info(
            self,
            user_id: str,
            user_email: str,
            admin: bool,
    ) -> UserInfo:
        """Retrieves user info by the unique user id"""
        user_info = await mongodb['user'].aggregate(
            [*pipeline_remove_id, {'$match': {'id': ObjectId(user_id)}}]).to_list(
            length=None)
        if user_info[0]:
            user_info = UserInfo(**user_info[0])
        else:
            raise HTTPException(status_code=404, detail="User not found")

        return user_info

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

        user_info = await mongodb['user'].aggregate([*pipeline_remove_id, {'$match': {'email': token_email}}]).to_list(
            length=None)
        if user_info[0]:
            user_info = UserInfo(**user_info[0])
        else:
            user_info = {
                'email': token_email,
                'username': token_username,
                'image': token_image,
                'rating': 0,
                'admin': False
            }
            res = await mongodb['user'].insert_one(user_info)
            user_info = UserInfo(id=str(res.inserted_id), **user_info)

        return VerifyResponse(auth_token=auth_token, iat_date=token_iat, exp_date=token_exp, user_info=user_info)

    async def put_user_info(
            self,
            user_id: str,
            user_email: str,
            admin: bool,
            new_user_info: NewUserInfo,
    ) -> UserInfo:
        """Updates user account info"""
        # Implementación de la función
        user = await mongodb['user'].find_one({'id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user["email"] != user_email or not admin:
            raise HTTPException(status_code=401, detail="User unauthorized for this operation")

        user = UserInfo(**user)
        user.username = new_user_info.username
        user.image = new_user_info.image
        await mongodb["user"].update_one({'id': ObjectId(user_id)}, {"username": new_user_info.username,
                                                                            "image": new_user_info.image})

        print(user)
        return user

    async def put_user_image(
            self,
            user_id: str,
            user_email: str,
            admin: bool,
            body: str,
    ) -> UserInfo:
        """Update the given user's profile picture"""
        user = await mongodb['user'].find_one({'id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user["email"] != user_email or not admin:
            raise HTTPException(status_code=401, detail="User unauthorized for this operation")

        user = UserInfo(**user)
        user.image = body
        await mongodb["user"].update_one({'id': ObjectId(user_id)}, {"image": body})

        return user

    async def put_user_username(
            self,
            user_id: str,
            user_email: str,
            admin: bool,
            body: str,
    ) -> UserInfo:
        """Update the given user's username"""
        user = await mongodb['user'].find_one({'id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user["email"] != user_email or not admin:
            raise HTTPException(status_code=401, detail="User unauthorized for this operation")

        user = UserInfo(**user)
        user.username = body
        await mongodb["user"].update_one({'id': ObjectId(user_id)}, {"username": body})

        return user
