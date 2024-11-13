# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
from xml.dom import NotFoundErr

from bson.errors import InvalidId

from openapi_server.apis.internal_api_base import BaseInternalApi
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
    "/comments/articles/{article_id}",
    responses={
        204: {"description": "No content, comments deleted successfully"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article not found"},
    },
    tags=["internal"],
    summary="Delete Articles Comments",
    response_model_by_alias=True,
)
async def delete_articles_comments(
    article_id: str = Path(..., description="The unique ID of the Article"),
) -> Response:
    """Deletes all comments from an article"""
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalApi.subclasses[0]().delete_articles_comments(article_id)
        return Response(status_code=204)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Article ID format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="Article not found")

