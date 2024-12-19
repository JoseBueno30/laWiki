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
from openapi_server.models.new_user_info import NewUserInfo
from openapi_server.models.user_info import UserInfo
from openapi_server.models.verify_response import VerifyResponse


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/users/{user_id}",
    responses={
        200: {"model": UserInfo, "description": "OK"},
        401: {"description": "Unauthorized, invalid token or no token provided"},
        404: {"description": "User not found"},
    },
    tags=["v1/public"],
    summary="Get user info",
    response_model_by_alias=True,
)
async def get_user_info(
    user_id: str = Path(..., description="User unique id"),
    user_email: str = Header(None, description="Client&#39;s authenticated email"),
    admin: bool = Header(None, description="True if user is an admin user, False otherwise"),
) -> UserInfo:
    """Retrieves user info by the unique account email"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_user_info(user_id, user_email, admin)


@router.post(
    "/v1/verify_token",
    responses={
        200: {"model": VerifyResponse, "description": "OK, valid token"},
        400: {"description": "Bad Request, invalid token"},
    },
    tags=["v1/public"],
    summary="Verify user token",
    response_model_by_alias=True,
)
async def post_verify_token(
    auth_token: str = Query(None, description="Google OAuth user authentication token", alias="auth_token"),
) -> VerifyResponse:
    """Returns user info from the user oatuh token"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().post_verify_token(auth_token)


@router.put(
    "/v1/users/{user_id}",
    responses={
        200: {"model": UserInfo, "description": "OK"},
        401: {"description": "User unauthorized for this operation"},
        404: {"description": "User not found"},
    },
    tags=["v1/public"],
    summary="Update user info",
    response_model_by_alias=True,
)
async def put_users_user_email(
    user_id: str = Path(..., description="User unique id"),
    user_email: str = Header(None, description="Client&#39;s authenticated email"),
    admin: bool = Header(None, description="True if user is an admin user, False otherwise"),
    new_user_info: NewUserInfo = Body(None, description=""),
) -> UserInfo:
    """Updates user account info"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().put_users_user_email(user_id, user_email, admin, new_user_info)


@router.put(
    "/v1/users/{user_id}/image",
    responses={
        200: {"description": "OK"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
    tags=["v1/public"],
    summary="Update user image",
    response_model_by_alias=True,
)
async def put_users_user_id_image(
    user_id: str = Path(..., description="The unique user ID"),
    user_email: str = Header(None, description="Client&#39;s authenticated email"),
    admin: bool = Header(None, description="True if user is an admin user, False otherwise"),
    body: str = Body(None, description=""),
) -> None:
    """Update the given user&#39;s profile picture"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().put_users_user_id_image(user_id, user_email, admin, body)


@router.put(
    "/v1/users/{user_id}/username",
    responses={
        200: {"description": "OK"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
    tags=["v1/public"],
    summary="Update user username",
    response_model_by_alias=True,
)
async def put_users_user_id_username(
    user_id: str = Path(..., description="The unique user ID"),
    user_email: str = Header(None, description="Client&#39;s authenticated email"),
    admin: bool = Header(None, description="True if user is an admin user, False otherwise"),
    body: str = Body(None, description=""),
) -> None:
    """Update the given user&#39;s username"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().put_users_user_id_username(user_id, user_email, admin, body)
