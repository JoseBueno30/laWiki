# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
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
from openapi_server.models.wiki import Wiki
from openapi_server.models.wiki_list import WikiList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


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
    try:
        result = await BaseDefaultApi.subclasses[0]().get_one_wiki_by_name(name)
    except LookupError:
        raise HTTPException(status_code=404, detail="Wiki Not Found")
    except:
        raise HTTPException(status_code=500, detail=MESSAGE_UNEXPECTED)

    return result


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
