# coding: utf-8
import json
from http.client import HTTPException
from typing import List
import time

from fastapi import Depends, Security  # noqa: F401
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (  # noqa: F401
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery  # noqa: F401
from openapi_server.models.extra_models import TokenModel
from openapi_server.impl.redis_config import redis_client
from openapi_server.impl.utils import forward_request, USERS_API_URL

bearer_auth = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_auth)) -> TokenModel:
    """
    Check and retrieve authentication information from custom bearer token.

    :param credentials Credentials provided by Authorization header
    :type credentials: HTTPAuthorizationCredentials
    :return: Decoded token information or None if token is invalid
    :rtype: TokenModel | None
    """
    token = credentials.credentials

    cached_token = redis_client.get(token)
    if not cached_token:
        body = {"auth_token": token}
        try:
            res = await forward_request(
                "PUT",
                f"{USERS_API_URL}/v1/verify_token",
                json=body.to_dict())

            token_data = {
                "iat_date" : res["iat_date"],
                "exp_date" : res["exp_date"],
                "user_info" : res["user_info"]
            }
            # Add token to the cache, with a TTL of 1.5 hours
            redis_client.set(token, json.dumps(token_data), ex=5400)
            return TokenModel(**token_data)
        except HTTPException:
            # invalid token
            return None

    token_data = json.loads(cached_token)
    if time.time() > token_data["exp_date"]:
        redis_client.delete(token)
        return None

    return TokenModel(**{**token_data, "auth_token" : None})






