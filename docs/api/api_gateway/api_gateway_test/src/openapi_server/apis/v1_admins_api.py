# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v1_admins_api_base import BaseV1AdminsApi
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
from pydantic import Field, StrictStr
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.new_tag import NewTag
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.tag import Tag
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
    tags=["v1/admins"],
    summary="Create Wiki",
    response_model_by_alias=True,
)
async def create_wiki(
    new_wiki: Optional[NewWiki] = Body(None, description=""),
) -> Wiki:
    """Create a new Wiki"""
    if not BaseV1AdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1AdminsApi.subclasses[0]().create_wiki(new_wiki)


@router.delete(
    "/v1/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted succesfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v1/admins"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag(
    id: StrictStr = Path(..., description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseV1AdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1AdminsApi.subclasses[0]().delete_tag(id)


@router.post(
    "/v1/tags/wikis/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["v1/admins"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag(
    id: Annotated[StrictStr, Field(description="The unique ID of the wiki.")] = Path(..., description="The unique ID of the wiki."),
    new_tag: Optional[NewTag] = Body(None, description=""),
) -> Tag:
    """Create a new tag in a given wiki."""
    if not BaseV1AdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1AdminsApi.subclasses[0]().post_wiki_tag(id, new_tag)


@router.delete(
    "/v1/wikis/{id_name}",
    responses={
        200: {"description": "Removed successfully. Returned deleted item."},
        400: {"description": "Bad Request."},
        403: {"description": "Forbidden. User is not authorized to delete wikis."},
        404: {"description": "Wiki not found."},
    },
    tags=["v1/admins"],
    summary="Remove Wiki",
    response_model_by_alias=True,
)
async def remove_wiki(
    id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")] = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> None:
    """Remove Wiki with the matching ID."""
    if not BaseV1AdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1AdminsApi.subclasses[0]().remove_wiki(id_name)


@router.put(
    "/v1/wikis/{id_name}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden. User is not authorized to edit wiki the requested wiki."},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["v1/admins"],
    summary="Update Wiki",
    response_model_by_alias=True,
)
async def update_wiki(
    id_name: Annotated[StrictStr, Field(description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified.")] = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    new_wiki: Optional[NewWiki] = Body(None, description=""),
) -> Wiki:
    """Update Wiki with wiki the matching ID"""
    if not BaseV1AdminsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1AdminsApi.subclasses[0]().update_wiki(id_name, new_wiki)
