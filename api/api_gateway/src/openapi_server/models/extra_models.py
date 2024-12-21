# coding: utf-8
from typing import Dict

from pydantic import BaseModel

class TokenModel(BaseModel):
    """Defines a token model."""
    iat_date: int
    exp_date: int
    user_info: Dict
    sub: str
