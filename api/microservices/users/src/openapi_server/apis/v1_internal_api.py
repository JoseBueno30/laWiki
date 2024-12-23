# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v1_internal_api_base import BaseV1InternalApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v1/users/{user_id}/rating",
    responses={
        200: {"model": UserInfo, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["v1/internal"],
    summary="Update user rating",
    response_model_by_alias=True,
)
async def put_user_rating(
    user_id: str = Path(..., description="Unique user id"),
    body: float = Body(None, description=""),
) -> UserInfo:
    """Update the given user&#39;s rating"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1InternalApi.subclasses[0]().put_user_rating(user_id, body)


@router.put(
    "/v1/verify_token",
    responses={
        200: {"model": VerifyResponse, "description": "OK"},
        401: {"description": "Unauthorized, invalid token"},
    },
    tags=["v1/internal"],
    summary="Verify user token",
    response_model_by_alias=True,
)
async def put_verify_token(
    body: str = Body(None, description=""),
) -> VerifyResponse:
    """Returns user info from the user oauth token"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1InternalApi.subclasses[0]().put_verify_token(body)
