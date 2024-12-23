# coding: utf-8
from typing import Dict

from pydantic import BaseModel

from openapi_server.models.user_info import UserInfo


class TokenModel(BaseModel):
    """Defines a token model."""
    iat_date: int
    exp_date: int
    user_info: UserInfo
