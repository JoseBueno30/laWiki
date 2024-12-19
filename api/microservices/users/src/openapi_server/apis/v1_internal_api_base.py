# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.new_rating import NewRating


class BaseV1InternalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1InternalApi.subclasses = BaseV1InternalApi.subclasses + (cls,)
    async def head_users_user_email(
        self,
        user_id: str,
    ) -> None:
        """Checks wheter the user email is registered in the application"""
        ...


    async def put_v1_users_user_email_rating(
        self,
        user_id: str,
        new_rating: NewRating,
    ) -> None:
        """Update the given user&#39;s rating"""
        ...
