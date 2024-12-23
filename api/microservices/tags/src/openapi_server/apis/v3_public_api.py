# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

from openapi_server.apis.v3_public_api_base import BaseV3PublicApi
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
from openapi_server.models.tag_list_v2 import TagListV2
from openapi_server.models.tag_v2 import TagV2


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v3/tags/articles/{id}",
    responses={
        200: {"model": TagListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Article not found"},
    },
    tags=["v3/public"],
    summary="Get Articles Tag",
    response_model_by_alias=True,
)
async def get_articles_tags_v3(
    id: str = Path(..., description=""),
    limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> TagListV2:
    """Retrieves all the tags from an article."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3PublicApi.subclasses[0]().get_articles_tags_v3(id, limit, offset)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Article ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Article not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/v3/tags/{id}",
    responses={
        200: {"model": TagV2, "description": "OK"},
        400: {"description": "Bad Request, invalid Tag ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["v3/public"],
    summary="Get Tag",
    response_model_by_alias=True,
)
async def get_tag_v3(
    id: str = Path(..., description=""),
) -> TagV2:
    """Get a tag by ID."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3PublicApi.subclasses[0]().get_tag_v3(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Tag ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/v3/tags/wikis/{id}",
    responses={
        200: {"model": TagListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Wiki not found"},
    },
    tags=["v3/public"],
    summary="Get Wikis Tags",
    response_model_by_alias=True,
)
async def get_wiki_tags_v3(
    id: str = Path(..., description="The unique ID of the wiki."),
    limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> TagListV2:
    """Retrieve all the tags from a wiki."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV3PublicApi.subclasses[0]().get_wiki_tags_v3(id, limit, offset)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad request, invalid Wiki ID format")
    except KeyError:
        raise HTTPException(status_code=404, detail="Wiki not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
