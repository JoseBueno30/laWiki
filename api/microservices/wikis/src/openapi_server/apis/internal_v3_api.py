# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId
from pydantic import StrictBool, StrictStr

from pymongo.errors import DuplicateKeyError, InvalidOperation
from openapi_server.apis.internal_v3_api_base import BaseInternalV3Api
import openapi_server.impl
from openapi_server.impl.misc import *

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
from openapi_server.models.id_tags_body_v2 import IdTagsBodyV2


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.put(
    "/v3/wikis/{id}/tags",
    responses={
        204: {"description": "No Content, tags assigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internalV3"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_wiki_tags_v3(
    response: Response,
    id: str = Path(..., description=""),
    user_email: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    id_tags_body_v2: IdTagsBodyV2 = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to a wiki"""
    if not BaseInternalV3Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalV3Api.subclasses[0]().assign_wiki_tags_v3(id, user_email, admin, id_tags_body_v2)
        response.status_code = 204
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)



@router.head(
    "/v3/wikis/{id_name}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Wiki ID"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internalV3"],
    summary="Check Wiki",
    response_model_by_alias=True,
)
async def check_wiki_by_idv3(
    response : Response,
    id_name: str = Path(..., description=""),
) -> None:
    """Check if a Wiki exits given its unique ID. """
    if not BaseInternalV3Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        if not await BaseInternalV3Api.subclasses[0]().check_wiki_by_idv3(id_name):
            response.status_code = 404
    except InvalidId:
        raise HTTPException(status_code=400, detail=MESSAGE_BAD_FORMAT)


@router.delete(
    "/v3/wikis/{id}/tags",
    responses={
        204: {"description": "No Content, tags unassigned"},
        400: {"description": "Bad Request, invalid parameters format"},
        403: {"description": "Forbidden"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internalV3"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_wiki_tags_v3(
    response: Response,
    id: str = Path(..., description=""),
    user_email: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    ids: List[str] = Query(None, description="List of Tag IDs", alias="ids"),
) -> None:
    """Unassigns a list of tags, given their IDs to a Wiki."""
    if not BaseInternalV3Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseInternalV3Api.subclasses[0]().unassign_wiki_tags_v3(id, user_email, admin, ids)
        response.status_code = 204
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)


@router.put(
    "/v3/wikis/{id}/ratings",
    responses={
        204: {"description": "No Content, rating updated"},
        400: {"description": "Bad Request, invalid parameter format"},
        401: {"description": "Unauthorized"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["internalV3"],
    summary="Update Rating",
    response_model_by_alias=True,
)
async def update_rating_v3(
    user_email: StrictStr = Header(..., description=""),
    admin: StrictBool = Header(..., description=""),
    id: str = Path(..., description=""),
    id_ratings_body: IdRatingsBody = Body(None, description=""),
) -> None:
    """Update the rating of a Wiki give its unique ID and a rating"""
    if not BaseInternalV3Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseInternalV3Api.subclasses[0]().update_rating_v3(user_email, admin, id, id_ratings_body)
