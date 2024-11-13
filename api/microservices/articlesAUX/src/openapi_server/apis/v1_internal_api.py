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
from openapi_server.models.id_ratings_body_v1 import IdRatingsBodyV1
from openapi_server.models.id_tags_body_v1 import IdTagsBodyV1


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v1/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Artcile Not Found"},
    },
    tags=["v1/internal"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_article_tags_v1(
    id: str = Path(..., description=""),
    id_tags_body_v1: IdTagsBodyV1 = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV1InternalApi.subclasses[0]().assign_article_tags(id, id_tags_body) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


@router.head(
    "/v1/articles/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Article ID"},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/internal"],
    summary="Check Article",
    response_model_by_alias=True,
)
async def check_article_by_idv1(
    id: str = Path(..., description=""),
) -> None:
    """Check if an Article exits given its unique ID. """
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if not await BaseV1InternalApi.subclasses[0]().check_article_by_id(id):
            raise HTTPException(status_code=404, detail="Artcile Not Found")
        else:
            return
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")


@router.delete(
    "/v1/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags unassigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/internal"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_article_tags_v1(
    id: str = Path(..., description=""),
    ids: list[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV1InternalApi.subclasses[0]().unassign_article_tags(id, ids) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


@router.put(
    "/v1/articles/{id}/ratings",
    responses={
        204: {"description": "No Content, rating updated"},
        400: {"description": "Bad Request, invalid parameter format"},
        401: {"description": "Unauthorized"},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/internal"],
    summary="Update Rating",
    response_model_by_alias=True,
)
async def update_rating_v1(
    id: str = Path(..., description=""),
    id_ratings_body_v1: IdRatingsBodyV1 = Body(None, description=""),
) -> None:
    """Update the rating of an Article give its unique ID and a rating"""
    if not BaseV1InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV1InternalApi.subclasses[0]().update_rating(id, id_ratings_body) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameter format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")
