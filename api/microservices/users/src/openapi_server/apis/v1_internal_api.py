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
from openapi_server.models.new_rating import NewRating


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.head(
    "/v1/users/{user_id}",
    responses={
        200: {"description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["v1/internal"],
    summary="Check user",
    response_model_by_alias=True,
)
async def head_users_user_email(
    user_id: str = Path(..., description="User unique id"),
) -> None:
    """Checks wheter the user email is registered in the application"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1InternalApi.subclasses[0]().head_users_user_email(user_id)


@router.put(
    "/v1/users/{user_id}/rating",
    responses={
        204: {"description": "No Content"},
        404: {"description": "Not Found"},
    },
    tags=["v1/internal"],
    summary="Update user rating",
    response_model_by_alias=True,
)
async def put_v1_users_user_email_rating(
    user_id: str = Path(..., description="Unique user id"),
    new_rating: NewRating = Body(None, description=""),
) -> None:
    """Update the given user&#39;s rating"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1InternalApi.subclasses[0]().put_v1_users_user_email_rating(user_id, new_rating)
