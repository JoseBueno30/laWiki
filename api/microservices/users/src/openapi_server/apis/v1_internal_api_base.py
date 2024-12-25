# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse


class BaseV1InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1InternalApi.subclasses = BaseV1InternalApi.subclasses + (cls,)
    async def put_user_rating(
        self,
        user_id: str,
        body: float,
    ) -> UserInfo:
        """Update the given user&#39;s rating"""
        ...


    async def put_verify_token(
        self,
        body: str,
    ) -> VerifyResponse:
        """Returns user info from the user oauth token"""
        ...
