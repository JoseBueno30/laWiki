# coding: utf-8
from fastapi.responses import JSONResponse
from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId
from pymongo import errors

from openapi_server.apis.editors_api_base import BaseEditorsApi
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
from openapi_server.models.article import Article
from openapi_server.models.article_version import ArticleVersion
from openapi_server.models.new_article import NewArticle
from openapi_server.models.new_article_version import NewArticleVersion


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/articles",
    responses={
        201: {"model": Article, "description": "Created"},
        400: {"description": "Bad Request, invalid paramaters"},
        403: {"description": "Forbidden"},
    },
    tags=["editors"],
    summary="Create Article",
    response_model_by_alias=True,
)
async def create_article(
    new_article: NewArticle = Body(None, description=""),
) -> Article:
    """Create a new Article in a given wiki"""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseEditorsApi.subclasses[0]().create_article(new_article)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate Key")
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/articles/{id}/versions",
    responses={
        201: {"model": ArticleVersion, "message": "Version successfully created."},
        400: {"description": "Bad Request, Invalid Parameters"},
        403: {"description": "Forbidden"},
    },
    tags=["editors"],
    summary="Create ArticleVersion for an Article",
    response_model_by_alias=True,
)
async def create_article_version(
    id: str = Path(..., description=""),
    new_article_version: NewArticleVersion = Body(None, description=""),
) -> ArticleVersion:
    """Create an ArticleVersion for a given Article and adds it to the list of versions of the Article."""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseEditorsApi.subclasses[0]().    create_article_version(id, new_article_version)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate Key")
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/articles/{id}",
    responses={
        200: {"description": "Article successfully deleted."},
        400: {"description": "Bad Request, invalid Article ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["editors"],
    summary="Delete Article",
    response_model_by_alias=True,
)
async def delete_article_by_id(
    id: str = Path(..., description=""),
) -> None:
    """Delete an Article identified by it&#39;s unique ID"""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseEditorsApi.subclasses[0]().delete_article_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Article Not Found")

@router.delete(
    "/articles/versions/{id}",
    responses={
        200: {"description": "ArticleVersion successfully deleted."},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["editors"],
    summary="Delete ArticleVersion",
    response_model_by_alias=True,
)
async def delete_article_version_by_id(
    id: str = Path(..., description=""),
) -> None:
    """Delete an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseEditorsApi.subclasses[0]().delete_article_version_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Article Not Found")

@router.put(
    "/articles/{article_id}/versions/{version_id}",
    responses={
        200: {"description": "ArticleVersion successfully restored"},
        400: {"description": "Bad Request, invalid Article or ArticleVersion ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["editors"],
    summary="Restore ArticleVersion",
    response_model_by_alias=True,
)
async def restore_article_version(
    article_id: str = Path(..., description=""),
    version_id: str = Path(..., description=""),
) -> None:
    """Restore an older ArticleVersion of an Article."""
    if not BaseEditorsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseEditorsApi.subclasses[0]().restore_article_version(article_id, version_id) is None:
            return JSONResponse(status_code=200, content={"detail": "ArticleVersion successfully restored"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article or ArticleVersion ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")