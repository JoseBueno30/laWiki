# coding: utf-8

from typing import Any, Coroutine, Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.impl.misc import *
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
from openapi_server.models.id_ratings_body import IdRatingsBody
from openapi_server.models.id_tags_body import IdTagsBody
from bson.errors import InvalidId

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v1/wikis/{id}/tags",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internal"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_wiki_tags(
    response : Response,
    id: str = Path(..., description=""),
    id_tags_body: IdTagsBody = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to a wiki"""
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalApi.subclasses[0]().assign_wiki_tags(id, id_tags_body)
        response.status_code = 204
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)


@router.head(
    "/v1/wikis/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Wiki ID"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internal"],
    summary="Check Wiki",
    response_model_by_alias=True,
)
async def check_wiki_by_id(
    response: Response,
    id: str = Path(..., description=""),
) -> None:
    """Check if a Wiki exits given its unique ID. """
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if not await BaseInternalApi.subclasses[0]().check_wiki_by_id(id):
            response.status_code = 404
    except InvalidId:
        raise HTTPException(status_code=400, detail=MESSAGE_BAD_FORMAT)


@router.delete(
    "/v1/wikis/{id}/tags",
    responses={
        204: {"description": "No Content, tags unassigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internal"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_article_tags(
    response: Response,
    id: str = Path(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to a Wiki."""
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalApi.subclasses[0]().unassign_article_tags(id, ids)
        response.status_code = 204
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)


@router.put(
    "/v1/wikis/{id}/ratings",
    responses={
        204: {"description": "No Content, rating updated"},
        400: {"description": "Bad Request, invalid parameter format"},
        401: {"description": "Unauthorized"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internal"],
    summary="Update Rating",
    response_model_by_alias=True,
)
async def update_rating(
    response: Response,
    id: str = Path(..., description=""),
    id_ratings_body: IdRatingsBody = Body(None, description=""),
) -> None:
    """Update the rating of a Wiki give its unique ID and a rating"""
    if not BaseInternalApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalApi.subclasses[0]().update_rating(id, id_ratings_body)
        response.status_code = 204
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)