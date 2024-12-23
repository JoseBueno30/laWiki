# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

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
from datetime import date
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.article_list_v2 import ArticleListV2
from openapi_server.models.article_v2 import ArticleV2
from openapi_server.models.article_version_list_v2 import ArticleVersionListV2
from openapi_server.models.article_version_v2 import ArticleVersionV2
from openapi_server.models.inline_response200_v2 import InlineResponse200V2


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/v3/articles/author/{id}",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, The given ID was not correct."},
        404: {"description": "Author Not Found."},
    },
    tags=["v3/public"],
    summary="Get Articles by Author",
    response_model_by_alias=True,
)
async def get_article_by_author_v3(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV2:
    """Get a list of Articles given an author&#39;s ID.  """
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_by_author_v3(id, offset, limit, order)


@router.get(
    "/v3/articles/{id}",
    responses={
        200: {"model": ArticleV2, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/public"],
    summary="Get Article",
    response_model_by_alias=True,
)
async def get_article_by_id_v3(
    id: StrictStr = Path(..., description=""),
) -> ArticleV2:
    """Get an Article identified by it&#39;s unique ID"""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_by_id_v3(id)


@router.get(
    "/v3/articles/versions/by-name/{name}",
    responses={
        200: {"model": ArticleVersionV2, "description": "OK"},
        400: {"description": "Bad Request, invalid Article name format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/public"],
    summary="Get ArticleVersion by name",
    response_model_by_alias=True,
)
async def get_article_by_name_v3(
    name: StrictStr = Path(..., description=""),
    wiki: Annotated[StrictStr, Field(description="The ID of the wiki of the Article")] = Query(None, description="The ID of the wiki of the Article", alias="wiki"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, any language if not specified")] = Query(None, description="Language of the ArticleVersion, any language if not specified", alias="lan"),
) -> ArticleVersionV2:
    """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_by_name_v3(name, wiki, lan)


@router.get(
    "/v3/articles/versions/{id}/body",
    responses={
        200: {"model": InlineResponse200V2, "description": "OK. Parsed Succesfully."},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v3/public"],
    summary="Get ArticleVersion body",
    response_model_by_alias=True,
)
async def get_article_version_body_by_idv3(
    id: StrictStr = Path(..., description=""),
    parsed: Annotated[Optional[StrictBool], Field(description="It indicates if the body must be parsed.")] = Query(False, description="It indicates if the body must be parsed.", alias="parsed"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the body, if parsed, original language if not specified")] = Query(None, description="Language of the body, if parsed, original language if not specified", alias="lan"),
) -> InlineResponse200V2:
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_version_body_by_idv3(id, parsed, lan)


@router.get(
    "/v3/articles/versions/{id}",
    responses={
        200: {"model": ArticleVersionV2, "description": "OK"},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v3/public"],
    summary="Get ArticleVersion",
    response_model_by_alias=True,
)
async def get_article_version_by_id_v3(
    id: StrictStr = Path(..., description=""),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, original language if not specified")] = Query(None, description="Language of the ArticleVersion, original language if not specified", alias="lan"),
) -> ArticleVersionV2:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_version_by_id_v3(id, lan)


@router.get(
    "/v3/articles/{id}/versions",
    responses={
        200: {"model": ArticleVersionListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article not Found"},
    },
    tags=["v3/public"],
    summary="Get Article&#39;s ArticleVersions",
    response_model_by_alias=True,
)
async def get_article_version_list_by_article_idv3(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[StrictInt], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset"),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleVersionListV2:
    """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_article_version_list_by_article_idv3(id, offset, limit, order)


@router.get(
    "/v3/articles/commented_by/{id}",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, inavalid User ID format"},
        404: {"description": "User Not Found"},
    },
    tags=["v3/public"],
    summary="Get Articles commented by User",
    response_model_by_alias=True,
)
async def get_articles_commented_by_user_v3(
    id: StrictStr = Path(..., description=""),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV2:
    """Get a list of the Articles commented by a given user."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().get_articles_commented_by_user_v3(id, offset, limit, order)


@router.get(
    "/v3/articles",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article Not Found"},
    },
    tags=["v3/public"],
    summary="Search for Articles",
    response_model_by_alias=True,
)
async def search_articles_v3(
    wiki_id: Annotated[Optional[StrictStr], Field(description="The ID of the wiki where the serch will be made")] = Query(None, description="The ID of the wiki where the serch will be made", alias="wiki_id"),
    name: Annotated[Optional[StrictStr], Field(description="Search query for the name of the article")] = Query(None, description="Search query for the name of the article", alias="name"),
    tags: Annotated[Optional[List[StrictStr]], Field(description="A comma-separated list of tag IDs to search for")] = Query(None, description="A comma-separated list of tag IDs to search for", alias="tags"),
    offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="The index of the first result to return. Use with limit to get the next page of search results.")] = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, strict=True, ge=0)]], Field(description="The maximum number of results to return.")] = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: Annotated[Optional[StrictStr], Field(description="Sorts the articles by different criteria")] = Query('none', description="Sorts the articles by different criteria", alias="order"),
    creation_date: Annotated[Optional[date], Field(description="Single date or range")] = Query(None, description="Single date or range", alias="creation_date"),
    author_name: Annotated[Optional[StrictStr], Field(description="Filter for the author of the Article")] = Query(None, description="Filter for the author of the Article", alias="author_name"),
    editor_name: Annotated[Optional[StrictStr], Field(description="Filter for the editors of the Article")] = Query(None, description="Filter for the editors of the Article", alias="editor_name"),
    lan: Annotated[Optional[StrictStr], Field(description="Language of the ArticleVersion, original language if not specified")] = Query(None, description="Language of the ArticleVersion, original language if not specified", alias="lan"),
) -> ArticleListV2:
    """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV3PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV3PublicApi.subclasses[0]().search_articles_v3(wiki_id, name, tags, offset, limit, order, creation_date, author_name, editor_name, lan)
