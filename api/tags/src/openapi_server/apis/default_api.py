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
from openapi_server.models.new_tag import NewTag
from openapi_server.models.tag import Tag
from openapi_server.models.tag_id_list import TagIDList
from openapi_server.models.tag_list import TagList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/tags/articles/{id}",
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request, invalid Tag ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["default"],
    summary="Assign Tags",
    response_model_by_alias=True,
)
async def assign_tags(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Assigns a list of tags, given their IDs, to an article."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().assign_tags(id, tag_id_list)


@router.delete(
    "/tags/{id}",
    responses={
        204: {"description": "No Content, tag deleted succesfully"},
        400: {"description": "Bad Request, invalid ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["default"],
    summary="Delete Tag",
    response_model_by_alias=True,
)
async def delete_tag(
    id: str = Path(..., description=""),
) -> None:
    """Delete a wiki tag."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().delete_tag(id)


@router.get(
    "/tags/articles/{id}",
    responses={
        200: {"model": List[Tag], "description": "OK"},
        404: {"description": "Article not found"},
    },
    tags=["default"],
    summary="Get Articles Tag",
    response_model_by_alias=True,
)
async def get_articles_tags(
    id: str = Path(..., description=""),
    limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> List[Tag]:
    """Retrieves all the tags from an article."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_articles_tags(id, limit, offset)


@router.get(
    "/tags/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, invalid Tag ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Tag not found"},
    },
    tags=["default"],
    summary="Get Tag",
    response_model_by_alias=True,
)
async def get_tag(
    id: str = Path(..., description=""),
) -> Tag:
    """Get a tag by ID. """
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_tag(id)


@router.get(
    "/tags/wikis/{id}",
    responses={
        200: {"model": TagList, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Wiki not found"},
    },
    tags=["default"],
    summary="Get Wikis Tags",
    response_model_by_alias=True,
)
async def get_wiki_tags(
    id: str = Path(..., description="The unique ID of the wiki."),
    limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
) -> TagList:
    """Retrieve all the tags from a wiki."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_wiki_tags(id, limit, offset)


@router.post(
    "/tags/wikis/{id}",
    responses={
        200: {"model": Tag, "description": "OK"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
    },
    tags=["default"],
    summary="Create Tag",
    response_model_by_alias=True,
)
async def post_wiki_tag(
    id: str = Path(..., description="The unique ID of the wiki."),
    new_tag: NewTag = Body(None, description=""),
) -> Tag:
    """Create a new tag in a given wiki."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_wiki_tag(id, new_tag)


@router.put(
    "/tags/articles/{id}",
    responses={
        204: {"description": "No Content, tag unassigned succesfully"},
        400: {"description": "Bad Request, invalid Tag ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or tag not found"},
    },
    tags=["default"],
    summary="Unassign Tags",
    response_model_by_alias=True,
)
async def unassign_tags(
    id: str = Path(..., description=""),
    tag_id_list: TagIDList = Body(None, description=""),
) -> None:
    """Unassigns a list of tags, given their IDs to an article."""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().unassign_tags(id, tag_id_list)
