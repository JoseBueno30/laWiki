# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
from xml.dom import NotFoundErr

from bson.errors import InvalidId
from starlette.responses import JSONResponse

from openapi_server.apis.v2_internal_api_base import BaseV2InternalApi
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
from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2


router = APIRouter()

ns_pkg = openapi_server.impl.v2_apis_impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v2/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Artcile Not Found"},
    },
    tags=["v2/internal"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_article_tags_v2(
    id: str = Path(..., description=""),
    id_tags_body_v2: IdTagsBodyV2 = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article"""
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV2InternalApi.subclasses[0]().assign_article_tags(id, id_tags_body_v2) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


@router.head(
    "/v2/articles/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Article ID"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/internal"],
    summary="Check Article",
    response_model_by_alias=True,
)
async def check_article_by_idv2(
    id: str = Path(..., description=""),
) -> None:
    """Check if an Article exits given its unique ID. """
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if not await BaseV2InternalApi.subclasses[0]().check_article_by_idv2(id):
            raise HTTPException(status_code=404, detail="Artcile Not Found")
        else:
            return
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")


@router.delete(
    "/v2/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags unassigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/internal"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_article_tags_v2(
    id: str = Path(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV2InternalApi.subclasses[0]().unassign_article_tags_v2(id, ids) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


@router.put(
    "/v2/articles/{id}/ratings",
    responses={
        204: {"description": "No Content, rating updated"},
        400: {"description": "Bad Request, invalid parameter format"},
        401: {"description": "Unauthorized"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/internal"],
    summary="Update Rating",
    response_model_by_alias=True,
)
async def update_rating_v2(
    id: str = Path(..., description=""),
    id_ratings_body_v2: IdRatingsBodyV2 = Body(None, description=""),
) -> None:
    """Update the rating of an Article give its unique ID and a rating"""
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if await BaseV2InternalApi.subclasses[0]().update_rating_v2(id, id_ratings_body_v2) is None:
            return JSONResponse(status_code=204, content={"detail":"No Content, tags assigned"})
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameter format")
    except NotFoundErr:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")

@router.delete(
    "/v2/articles/wiki/{id}",
    responses={
        200: {"description": "Articles Successfully Deleted"},
        400: {"description": "Bad Request, invalid Wiki ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Articles Not Found"},
    },
    tags=["internal"],
    summary="Delete Articles from Wiki",
    response_model_by_alias=True,
)
async def delete_articles_from_wiki(
    id: str = Path(..., description=""),
) -> None:
    if not BaseV2InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2InternalApi.subclasses[0]().delete_articles_from_wiki(id)