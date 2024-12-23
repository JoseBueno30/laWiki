# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v1.v1_internal_api_base import BaseV1InternalApi
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


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/v1/comments/articles/{article_id}",
    responses={
        204: {"description": "No content, comments deleted successfully"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article not found"},
    },
    tags=["v1/internal"],
    summary="Delete Articles Comments",
    response_model_by_alias=True,
)
async def v1_delete_articles_comments(
    article_id: str = Path(..., description="The unique ID of the Article"),
) -> None:
    """Deletes all comments from an article"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1InternalApi.subclasses[0]().v1_delete_articles_comments(article_id)
