# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_rating import NewRating
from openapi_server.models.user_info import UserInfo


class BaseV1InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1InternalApi.subclasses = BaseV1InternalApi.subclasses + (cls,)
    async def check_user(
        self,
        user_id: str,
        user_email: str,
    ) -> None:
        """Checks wheter the user email is registered in the application"""
        ...


    async def put_user_rating(
        self,
        user_id: str,
        new_rating: NewRating,
    ) -> UserInfo:
        """Update the given user&#39;s rating"""
        ...
