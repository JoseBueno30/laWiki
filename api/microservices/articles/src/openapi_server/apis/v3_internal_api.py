# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v3_internal_api_base import BaseV3InternalApi
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
from pydantic import Field, StrictBool, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.models_v2.id_ratings_body_v2 import IdRatingsBodyV2
from openapi_server.models.models_v2.id_tags_body_v2 import IdTagsBodyV2


router = APIRouter()

ns_pkg = openapi_server.impl.v3_apis_impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v3/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Artcile Not Found"},
    },
    tags=["v3/internal"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_article_tags_v3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    id_tags_body_v2: Optional[IdTagsBodyV2] = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article"""
    if not BaseV3InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3InternalApi.subclasses[0]().assign_article_tags_v3(id, user_id, admin, id_tags_body_v2)


@router.head(
    "/v3/articles/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Article ID"},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/internal"],
    summary="Check Article",
    response_model_by_alias=True,
)
async def check_article_by_idv3(
    id: StrictStr = Path(..., description=""),
) -> None:
    """Check if an Article exits given its unique ID. """
    if not BaseV3InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3InternalApi.subclasses[0]().check_article_by_idv3(id)


@router.delete(
    "/v3/articles/wiki/{id}",
    responses={
        200: {"description": "Articles Successfully Deleted"},
        400: {"description": "Bad Request, invalid Wiki ID format. "},
        403: {"description": "Forbidden"},
        404: {"description": "Articles Not Found"},
    },
    tags=["v3/internal"],
    summary="Delete Articles from Wiki",
    response_model_by_alias=True,
)
async def delete_articles_from_wiki_v3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
) -> None:
    if not BaseV3InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3InternalApi.subclasses[0]().delete_articles_from_wiki_v3(id, user_id, admin)


@router.delete(
    "/v3/articles/{id}/tags",
    responses={
        204: {"description": "No Content, tags unassigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/internal"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_article_tags_v3(
    id: StrictStr = Path(..., description=""),
    ids: Annotated[List[StrictStr], Field(max_length=50, description="List of Tag IDs")] = Query(None, description="List of Tag IDs", alias="ids"),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseV3InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3InternalApi.subclasses[0]().unassign_article_tags_v3(id, ids, user_id, admin)


@router.put(
    "/v3/articles/{id}/ratings",
    responses={
        204: {"description": "No Content, rating updated"},
        400: {"description": "Bad Request, invalid parameter format"},
        401: {"description": "Unauthorized"},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/internal"],
    summary="Update Rating",
    response_model_by_alias=True,
)
async def update_rating_v3(
    id: StrictStr = Path(..., description=""),
    user_id: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    id_ratings_body_v2: Optional[IdRatingsBodyV2] = Body(None, description=""),
) -> None:
    """Update the rating of an Article give its unique ID and a rating"""
    if not BaseV3InternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3InternalApi.subclasses[0]().update_rating_v3(id, user_id, admin, id_ratings_body_v2)
