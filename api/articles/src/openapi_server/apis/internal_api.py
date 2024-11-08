# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

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


@router.head(
    "/articles/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Article ID"},
        404: {"description": "Article Not Found"},
    },
    tags=["internal"],
    summary="Check Article",
    response_model_by_alias=True,
)
async def check_article_by_id(
    id: str = Path(..., description=""),
) -> None:
    """Check if an Article exits given its unique ID. """
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseInternalApi.subclasses[0]().check_article_by_id(id)
