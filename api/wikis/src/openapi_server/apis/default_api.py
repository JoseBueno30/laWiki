# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
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
from openapi_server.models.new_wiki import NewWiki
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/wikis",
    responses={
        201: {"model": Wiki, "description": "Created succesfully."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
    },
    tags=["default"],
    summary="Create Wiki",
    response_model_by_alias=True,
)
async def create_wiki(
    name: str = Query(None, description="String to be searched within the wiki&#39;s name.", alias="name"),
    limit: int = Query(20, description="Maximum amount of results to be returned.", alias="limit", ge=1, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    new_wiki: NewWiki = Body(None, description=""),
) -> Wiki:
    """Create a new Wiki"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().create_wiki(name, limit, offset, new_wiki)


@router.get(
    "/wikis/{name}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"model": Wiki, "description": "Bad Request"},
        404: {"description": "Wiki Not Found"},
    },
    tags=["default"],
    summary="Get Wiki by name",
    response_model_by_alias=True,
)
async def get_one_wiki_by_name(
    name: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> Wiki:
    """Get the Wiki with the given name."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_one_wiki_by_name(name)


@router.get(
    "/wikis/{id}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["default"],
    summary="Get Wiki",
    response_model_by_alias=True,
)
async def get_wiki(
    id: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> Wiki:
    """Get Wiki with the matching ID."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_wiki(id)


@router.delete(
    "/wikis/{id}",
    responses={
        200: {"description": "Removed successfully. Returned deleted item."},
        400: {"description": "Bad Request."},
        403: {"description": "Forbidden. User is not authorized to delete wikis."},
        404: {"description": "Wiki not found."},
    },
    tags=["default"],
    summary="Remove Wiki",
    response_model_by_alias=True,
)
async def remove_wiki(
    id: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
) -> None:
    """Remove Wiki with the matching ID."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().remove_wiki(id)


@router.get(
    "/wikis",
    responses={
        200: {"model": WikiList, "description": "Succesful operation."},
        400: {"description": "Bad Request, invalid parameters"},
        418: {"description": "The server refused to brew coffee. &lt;br/&gt; *Yes, this is a joke. Yes, this is a reserved HTTP response code since 1998.* &lt;br/&gt; *See [RFC 2324](https://datatracker.ietf.org/doc/html/rfc2324) for more information. Actually, do not.*"},
    },
    tags=["default"],
    summary="Search for Wikis",
    response_model_by_alias=True,
)
async def search_wikis(
    name: str = Query(None, description="String to be searched within the wiki&#39;s name.", alias="name"),
    offset: int = Query(20, description="Maximum amount of results to be returned.", alias="offset", ge=1, le=100),
    limit: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="limit", ge=0),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
    creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
    author_name: str = Query(None, description="Filter for the author of the Wiki", alias="author_name"),
) -> WikiList:
    """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().search_wikis(name, offset, limit, order, creation_date, author_name)


@router.put(
    "/wikis/{id}",
    responses={
        200: {"model": Wiki, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden. User is not authorized to edit wiki the requested wiki."},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["default"],
    summary="Update Wiki",
    response_model_by_alias=True,
)
async def update_wiki(
    id: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    new_wiki: NewWiki = Body(None, description=""),
) -> Wiki:
    """Update Wiki with wiki the matching ID"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().update_wiki(id, new_wiki)