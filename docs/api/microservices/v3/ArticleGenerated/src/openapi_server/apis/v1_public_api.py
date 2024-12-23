# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.v1_public_api_base import BaseV1PublicApi
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
from datetime import date
from pydantic import Field, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article_list_v1 import ArticleListV1
from openapi_server.models.article_v1 import ArticleV1
from openapi_server.models.article_version_list_v1 import ArticleVersionListV1
from openapi_server.models.article_version_v1 import ArticleVersionV1


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v1/articles/author/{id}",
    responses={
        200: {"model": ArticleListV1, "description": "OK"},
        400: {"description": "Bad Request, The given ID was not correct."},
        404: {"description": "Author Not Found."},
    },
    tags=["v1/public"],
    summary="Get Articles by Author",
    response_model_by_alias=True,
)
async def get_article_by_author_v1(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(0, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV1:
    """Get a list of Articles given an author&#39;s ID.  """
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_article_by_author_v1(id, offset, limit, order)


@router.get(
    "/v1/articles/{id}",
    responses={
        200: {"model": ArticleV1, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/public"],
    summary="Get Article",
    response_model_by_alias=True,
)
async def get_article_by_id_v1(
    id: StrictStr = Path(..., description=""),
) -> ArticleV1:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_article_by_id_v1(id)


@router.get(
    "/v1/articles/versions/by-name/{name}",
    responses={
        200: {"model": ArticleVersionV1, "description": "OK"},
        400: {"description": "Bad Request, invalid Article name format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/public"],
    summary="Get ArticleVersion by name",
    response_model_by_alias=True,
)
async def get_article_by_name_v1(
    name: StrictStr = Path(..., description=""),
    wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")] = Query(None, description="The ID of the wiki of the Article", alias="wiki"),
) -> ArticleVersionV1:
    """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_article_by_name_v1(name, wiki)


@router.get(
    "/v1/articles/versions/{id}",
    responses={
        200: {"model": ArticleVersionV1, "description": "OK"},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v1/public"],
    summary="Get ArticleVersion",
    response_model_by_alias=True,
)
async def get_article_version_by_id_v1(
    id: StrictStr = Path(..., description=""),
) -> ArticleVersionV1:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_article_version_by_id_v1(id)


@router.get(
    "/v1/articles/{id}/versions",
    responses={
        200: {"model": ArticleVersionListV1, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article not Found"},
    },
    tags=["v1/public"],
    summary="Get Article&#39;s ArticleVersions",
    response_model_by_alias=True,
)
async def get_article_version_list_by_article_idv1(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleVersionListV1:
    """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date and support pagination."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_article_version_list_by_article_idv1(id, offset, limit, order)


@router.get(
    "/v1/articles/commented_by/{id}",
    responses={
        200: {"model": ArticleListV1, "description": "OK"},
        400: {"description": "Bad Request, inavalid User ID format"},
        404: {"description": "User Not Found"},
    },
    tags=["v1/public"],
    summary="Get Articles commented by User",
    response_model_by_alias=True,
)
async def get_articles_commented_by_user_v1(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV1:
    """Get a list of the Articles commented by a given user."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().get_articles_commented_by_user_v1(id, offset, limit, order)


@router.get(
    "/v1/articles",
    responses={
        200: {"model": ArticleListV1, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article Not Found"},
    },
    tags=["v1/public"],
    summary="Search for Articles",
    response_model_by_alias=True,
)
async def search_articles_v1(
    wiki_id: Annotated[Optional[StrictStr], Field(description="The ID of the wiki where the serch will be made")] = Query(None, description="The ID of the wiki where the serch will be made", alias="wiki_id"),
    name: Annotated[Optional[StrictStr], Field(description="Search query for the name of the article")] = Query(None, description="Search query for the name of the article", alias="name"),
    tags: Annotated[Optional[List[StrictStr]], Field(description="A comma-separated list of tag IDs to search for")] = Query(None, description="A comma-separated list of tag IDs to search for", alias="tags"),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query('none', description="Sorts the articles by different criteria", alias="order"),
    creation_date: Annotated[Optional[date], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
    author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Article")] = Query(None, description="Filter for the author of the Article", alias="author_name"),
    editor_name: Annotated[Optional[StrictStr], Field(description="Filter for the editors of the Article")] = Query(None, description="Filter for the editors of the Article", alias="editor_name"),
) -> ArticleListV1:
    """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV1PublicApi.subclasses[0]().search_articles_v1(wiki_id, name, tags, offset, limit, order, creation_date, author_name, editor_name)
