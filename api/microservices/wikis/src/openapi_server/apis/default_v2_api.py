# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_v2_api_base import BaseDefaultV2Api
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
from openapi_server.models.new_wiki_v2 import NewWikiV2
from openapi_server.models.wiki_list_v2 import WikiListV2
from openapi_server.models.wiki_v2 import WikiV2


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/v2/wikis",
    responses={
        201: {"model": WikiV2, "description": "Created succesfully."},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
    },
    tags=["defaultV2"],
    summary="Create Wiki",
    response_model_by_alias=True,
)
async def create_wiki_v2(
    new_wiki_v2: NewWikiV2 = Body(None, description=""),
) -> WikiV2:
    """Create a new Wiki"""
    if not BaseDefaultV2Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultV2Api.subclasses[0]().create_wiki_v2(new_wiki_v2)


@router.get(
    "/v2/wikis/{id_name}",
    responses={
        200: {"model": WikiV2, "description": "Succesful operation."},
        400: {"description": "Bad Request"},
        404: {"description": "Bad Request. Wiki not found."},
    },
    tags=["defaultV2"],
    summary="Get Wiki",
    response_model_by_alias=True,
)
async def get_wiki_v2(
    id_name: str = Path(..., description="Identifier of the requested wiki, may be its name or its ID. Keep in mind wiki names may be modified."),
    lang: str = Query(None, description="Language of the wiki to retrieve, may generate a new translation if it  hasn&#39;t been requested before.", alias="lang"),
) -> WikiV2:
    """Get Wiki with the matching ID."""
    if not BaseDefaultV2Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultV2Api.subclasses[0]().get_wiki_v2(id_name, lang)


@router.get(
    "/v2/wikis",
    responses={
        200: {"model": WikiListV2, "description": "Succesful operation."},
        400: {"description": "Bad Request, invalid parameters"},
        418: {"description": "The server refused to brew coffee. &lt;br/&gt; *Yes, this is a joke. Yes, this is a reserved HTTP response code since 1998.* &lt;br/&gt; *See [RFC 2324](https://datatracker.ietf.org/doc/html/rfc2324) for more information. Actually, do not.*"},
    },
    tags=["defaultV2"],
    summary="Search for Wikis",
    response_model_by_alias=True,
)
async def search_wikis_v2(
    name: str = Query(None, description="String to be searched within the wiki&#39;s name.", alias="name"),
    offset: int = Query(20, description="Maximum amount of results to be returned.", alias="offset", ge=1, le=100),
    limit: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="limit", ge=0),
    order: str = Query(None, description="Sorts the wikis by different criteria", alias="order"),
    creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
    author_name: str = Query(None, description="Filter for the author of the Wiki", alias="author_name"),
) -> WikiListV2:
    """Get a list of Wikis that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseDefaultV2Api.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultV2Api.subclasses[0]().search_wikis_v2(name, offset, limit, order, creation_date, author_name)