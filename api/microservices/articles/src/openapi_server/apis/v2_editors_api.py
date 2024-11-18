# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId
from pymongo import errors
from starlette.responses import JSONResponse

from openapi_server.apis.v2_editors_api_base import BaseV2EditorsApi
import openapi_server.impl.v2_apis_impl

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

from openapi_server.models.models_v2.extra_models import TokenModel  # noqa: F401
from openapi_server.models.models_v2.article_v2 import ArticleV2
from openapi_server.models.models_v2.article_version_v2 import ArticleVersionV2
from openapi_server.models.models_v2.new_article_v2 import NewArticleV2
from openapi_server.models.models_v2.new_article_version_v2 import NewArticleVersionV2


router = APIRouter()

ns_pkg = openapi_server.impl.v2_apis_impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v2/articles",
    responses={
        201: {"model": ArticleV2, "description": "Created"},
        400: {"description": "Bad Request, invalid paramaters"},
        403: {"description": "Forbidden"},
    },
    tags=["v2/editors"],
    summary="Create Article",
    response_model_by_alias=True,
)
async def create_article_v2(
    new_article_v2: NewArticleV2 = Body(None, description=""),
) -> ArticleV2:
    """Create a new Article in a given wiki"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().create_article(new_article_v2)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate Key")
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/v2/articles/{id}/versions",
    responses={
        201: {"model": ArticleVersionV2, "description": "Version successfully created."},
        400: {"description": "Bad Request, Invalid Parameters"},
        403: {"description": "Forbidden"},
    },
    tags=["v2/editors"],
    summary="Create ArticleVersion for an Article",
    response_model_by_alias=True,
)
async def create_article_version_v2(
    id: str = Path(..., description=""),
    new_article_version_v2: NewArticleVersionV2 = Body(None, description=""),
) -> ArticleVersionV2:
    """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2EditorsApi.subclasses[0]().    create_article_version(id, new_article_version_v2)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate Key")
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/v2/articles/{id}",
    responses={
        200: {"description": "Article successfully deleted."},
        400: {"description": "Bad Request, invalid Article ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/editors"],
    summary="Delete Article",
    response_model_by_alias=True,
)
async def delete_article_by_idv2(
    id: str = Path(..., description=""),
) -> None:
    """Delete an Article identified by it&#39;s unique ID"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseV2EditorsApi.subclasses[0]().delete_article_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Article Not Found")


@router.delete(
    "/v2/articles/versions/{id}",
    responses={
        200: {"description": "ArticleVersion successfully deleted."},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v2/editors"],
    summary="Delete ArticleVersion",
    response_model_by_alias=True,
)
async def delete_article_version_by_id_v2(
    id: str = Path(..., description=""),
) -> None:
    """Delete an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseV2EditorsApi.subclasses[0]().delete_article_version_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Article Not Found")


@router.put(
    "/v2/articles/{article_id}/versions/{version_id}",
    responses={
        200: {"description": "ArticleVersion successfully restored"},
        400: {"description": "invalid Article or ArticleVersion ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v2/editors"],
    summary="Restore ArticleVersion",
    response_model_by_alias=True,
)
async def restore_article_version_v2(
    article_id: str = Path(..., description=""),
    version_id: str = Path(..., description=""),
) -> None:
    """Restore an older ArticleVersion of an Article."""
    if not BaseV2EditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV2EditorsApi.subclasses[0]().restore_article_version(article_id, version_id) is None:
            return JSONResponse(status_code=200, content={"detail": "ArticleVersion successfully restored"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article or ArticleVersion ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")