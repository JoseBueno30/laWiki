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
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(0, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV1:
    """Get a list of Articles given an author&#39;s ID.  """
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1PublicApi.subclasses[0]().get_article_by_author(id, offset, limit, order)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Author ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


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
    id: str = Path(..., description=""),
) -> ArticleV1:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1PublicApi.subclasses[0]().get_article_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


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
    name: str = Path(..., description=""),
    wiki: str = Query(None, description="The ID of the wiki of the Article", alias="wiki"),
) -> ArticleVersionV1:
    """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    
    #TODO: throw InvalidParameterValue if the name or wiki_id is invalid
    try:
        return await BaseV1PublicApi.subclasses[0]().get_article_by_name(name, wiki)
    except InvalidParameterValue:
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article name format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


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
    id: str = Path(..., description=""),
) -> ArticleVersionV1:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1PublicApi.subclasses[0]().get_article_version_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid ArticleVersion ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


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
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset"),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleVersionListV1:
    """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
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
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
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
    wiki_id: str = Query(None, description="The ID of the wiki where the serch will be made", alias="wiki_id"),
    name: str = Query(None, description="Search query for the name of the article", alias="name"),
    tags: list[str] = Query(None, description="A comma-separated list of tag IDs to search for", alias="tags"),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query('none', description="Sorts the articles by different criteria", alias="order"),
    creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
    author_name: str = Query(None, description="Filter for the author of the Article", alias="author_name"),
    editor_name: str = Query(None, description="Filter for the editors of the Article", alias="editor_name"),
) -> ArticleListV1:
    """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV1PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV1PublicApi.subclasses[0]().search_articles(wiki_id, name, tags, offset, limit, order, creation_date, author_name, editor_name)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid input parameters.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")
