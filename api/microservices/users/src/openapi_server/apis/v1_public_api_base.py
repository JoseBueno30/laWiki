# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_user_info import NewUserInfo
from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def get_user_info(
        self,
        user_id: str,
        user_email: str,
        admin: bool,
    ) -> UserInfo:
        """Retrieves user info by the unique account email"""
        ...


    async def post_verify_token(
        self,
        auth_token: str,
    ) -> VerifyResponse:
        """Returns user info from the user oatuh token"""
        ...


    async def put_user_info(
        self,
        user_id: str,
        user_email: str,
        admin: bool,
        new_user_info: NewUserInfo,
    ) -> UserInfo:
        """Updates user account info"""
        ...


    async def put_user_image(
        self,
        user_id: str,
        user_email: str,
        admin: bool,
        body: str,
    ) -> UserInfo:
        """Update the given user&#39;s profile picture"""
        ...


    async def put_user_username(
        self,
        user_id: str,
        user_email: str,
        admin: bool,
        body: str,
    ) -> UserInfo:
        """Update the given user&#39;s username"""
        ...
