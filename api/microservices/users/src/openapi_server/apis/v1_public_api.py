# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
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
from openapi_server.models.public_user_info import PublicUserInfo


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/users/{user_id}",
    responses={
        200: {"model": PublicUserInfo, "description": "OK"},
        403: {"description": "Forbidden"},
        404: {"description": "User not found"},
    },
    tags=["v1/public"],
    summary="Get user info",
    response_model_by_alias=True,
)
async def get_user_info(
    user_id: str = Path(..., description="User unique id"),
) -> PublicUserInfo:
    """Retrieves user info by the unique account email"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_user_info(user_id)
