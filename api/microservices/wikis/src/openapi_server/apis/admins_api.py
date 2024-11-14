# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
from bson.errors import InvalidId

from pymongo.errors import DuplicateKeyError
from openapi_server.apis.admins_api_base import BaseAdminsApi
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
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v1/wikis",
    responses={
        201: {"model": Wiki, "description": "Created succesfully."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
    },
    tags=["admins"],
    summary="Create Wiki",
    response_model_by_alias=True,
)
async def create_wiki(
    response: Response,
    name: str = Query(None, description="String to be searched within the wiki&#39;s name.", alias="name"),
    limit: int = Query(20, description="Maximum amount of results to be returned.", alias="limit", ge=1, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    new_wiki: NewWiki = Body(None, description=""),
) -> Wiki:
    """Create a new Wiki"""
    if not BaseAdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        result = await BaseAdminsApi.subclasses[0]().create_wiki(name, limit, offset, new_wiki)
        response.status_code = 201
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Wiki name unavailable")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=MESSAGE_UNEXPECTED)

    return result


@router.delete(
    "/v1/wikis/{id}",
    responses={
        200: {"description": "Removed successfully. Returned deleted item."},
        400: {"description": "Bad Request."},
        403: {"description": "Forbidden. User is not authorized to delete wikis."},
        404: {"description": "Wiki not found."},
    },
    tags=["admins"],
    summary="Remove Wiki",
    response_model_by_alias=True,
)
async def remove_wiki(
    response : Response,
    id: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> None:
    """Remove Wiki with the matching ID."""
    if not BaseAdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        await BaseAdminsApi.subclasses[0]().remove_wiki(id)
    except LookupError:
        response.status_code = 404
    except InvalidId as e:
        raise_http_exception(400, MESSAGE_BAD_FORMAT, e)
    except Exception as e:
        raise_http_exception(500, MESSAGE_UNEXPECTED, e)


@router.put(
    "/v1/wikis/{id}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden. User is not authorized to edit wiki the requested wiki."},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["admins"],
    summary="Update Wiki",
    response_model_by_alias=True,
)
async def update_wiki(
    id: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    new_wiki: NewWiki = Body(None, description=""),
) -> Wiki:
    """Update Wiki with wiki the matching ID"""
    if not BaseAdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminsApi.subclasses[0]().update_wiki(id, new_wiki)
