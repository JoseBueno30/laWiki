# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.public_user_info import PublicUserInfo


class BaseV1PublicApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseV1PublicApi.subclasses = BaseV1PublicApi.subclasses + (cls,)
    async def get_user_info(
        self,
        user_id: str,
    ) -> PublicUserInfo:
        """Retrieves user info by the unique account email"""
        ...
