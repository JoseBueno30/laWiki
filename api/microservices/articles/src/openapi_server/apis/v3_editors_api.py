# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v3_editors_api_base import BaseV3EditorsApi
import openapi_server.impl.v3_apis_impl

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
from pydantic import StrictBool, StrictStr
from typing import Any, Optional
from openapi_server.models.article_v2 import ArticleV2
from openapi_server.models.article_version_v2 import ArticleVersionV2
from openapi_server.models.new_article_v2 import NewArticleV2
from openapi_server.models.new_article_version_v2 import NewArticleVersionV2


router = APIRouter()

ns_pkg = openapi_server.impl.v3_apis_impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v3/articles",
    responses={
        201: {"model": ArticleV2, "description": "Created"},
        400: {"description": "Bad Request, invalid paramaters"},
        403: {"description": "Forbidden"},
    },
    tags=["v3/editors"],
    summary="Create Article",
    response_model_by_alias=True,
)
async def create_article_v3(
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    new_article_v2: Optional[NewArticleV2] = Body(None, description=""),
) -> ArticleV2:
    """Create a new Article in a given wiki"""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3EditorsApi.subclasses[0]().create_article_v3(user_id, admin, new_article_v2)


@router.post(
    "/v3/articles/{id}/versions",
    responses={
        201: {"model": ArticleVersionV2, "description": "Version successfully created."},
        400: {"description": "Bad Request, Invalid Parameters"},
        403: {"description": "Forbidden"},
    },
    tags=["v3/editors"],
    summary="Create ArticleVersion for an Article",
    response_model_by_alias=True,
)
async def create_article_version_v3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    new_article_version_v2: Optional[NewArticleVersionV2] = Body(None, description=""),
) -> ArticleVersionV2:
    """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3EditorsApi.subclasses[0]().create_article_version_v3(id, user_id, admin, new_article_version_v2)


@router.delete(
    "/v3/articles/{id}",
    responses={
        200: {"description": "Article successfully deleted."},
        400: {"description": "Bad Request, invalid Article ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/editors"],
    summary="Delete Article",
    response_model_by_alias=True,
)
async def delete_article_by_idv3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
) -> None:
    """Delete an Article identified by it&#39;s unique ID"""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3EditorsApi.subclasses[0]().delete_article_by_idv3(id, user_id, admin)


@router.delete(
    "/v3/articles/versions/{id}",
    responses={
        200: {"description": "ArticleVersion successfully deleted."},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v3/editors"],
    summary="Delete ArticleVersion",
    response_model_by_alias=True,
)
async def delete_article_version_by_id_v3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
) -> None:
    """Delete an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3EditorsApi.subclasses[0]().delete_article_version_by_id_v3(id, user_id, admin)


@router.put(
    "/v3/articles/{article_id}/versions/{version_id}",
    responses={
        200: {"description": "ArticleVersion successfully restored"},
        400: {"description": "invalid Article or ArticleVersion ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v3/editors"],
    summary="Restore ArticleVersion",
    response_model_by_alias=True,
)
async def restore_article_version_v3(
    article_id: StrictStr = Path(..., description=""),
    version_id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
) -> None:
    """Restore an older ArticleVersion of an Article."""
    if not BaseV3EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3EditorsApi.subclasses[0]().restore_article_version_v3(article_id, version_id, user_id, admin)
