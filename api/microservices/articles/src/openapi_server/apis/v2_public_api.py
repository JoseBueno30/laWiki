# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId
from websockets import InvalidParameterValue

from openapi_server.apis.v2_public_api_base import BaseV2PublicApi
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
    "/v2/articles/author/{id}",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, The given ID was not correct."},
        404: {"description": "Author Not Found."},
    },
    tags=["v2/public"],
    summary="Get Articles by Author",
    response_model_by_alias=True,
)
async def get_article_by_author_v2(
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(0, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV2:
    """Get a list of Articles given an author&#39;s ID.  """
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2PublicApi.subclasses[0]().get_article_by_author(id, offset, limit, order)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Author ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


@router.get(
    "/v2/articles/{id}",
    responses={
        200: {"model": ArticleV2, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Get Article",
    response_model_by_alias=True,
)
async def get_article_by_id_v2(
    id: str = Path(..., description=""),
) -> ArticleV2:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2PublicApi.subclasses[0]().get_article_by_id(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


@router.get(
    "/v2/articles/versions/by-name/{name}",
    responses={
        200: {"model": ArticleVersionV2, "description": "OK"},
        400: {"description": "Bad Request, invalid Article name format. "},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion by name",
    response_model_by_alias=True,
)
async def get_article_by_name_v2(
    name: str = Path(..., description=""),
    wiki: str = Query(None, description="The ID of the wiki of the Article", alias="wiki"),
    lan: str = Query(None, description="Language of the ArticleVersion, original language if not specified", alias="lan"),
) -> ArticleVersionV2:
    """Get the most recent ArticleVersion the Article with the given name from the specified Wiki."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    
    #TODO: throw InvalidParameterValue if the name or wiki_id is invalid
    try:
        return await BaseV2PublicApi.subclasses[0]().get_article_by_name(name, wiki, lan)
    except InvalidParameterValue:
        raise HTTPException(status_code=400, detail="Bad Request, invalid Article name format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")


@router.get(
    "/v2/articles/versions/{id}/body",
    responses={
        200: {"model": InlineResponse200V2, "description": "OK. Parsed Succesfully."},
        404: {"description": "ArticleVersion Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion body",
    response_model_by_alias=True,
)
async def get_article_version_body_by_idv2(
    id: str = Path(..., description=""),
    parsed: bool = Query(False, description="It indicates if the body must be parsed.", alias="parsed"),
    lan: str = Query(None, description="Language of the body, if parsed", alias="lan"),
) -> InlineResponse200V2:
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2PublicApi.subclasses[0]().get_article_version_body_by_idv2(id, parsed, lan)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid ArticleVersion ID format.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="ArticleVersion Not Found")


@router.get(
    "/v2/articles/versions/{id}",
    responses={
        200: {"model": ArticleVersionV2, "description": "OK"},
        400: {"description": "Bad Request, invalid ArticleVersion ID format. "},
        404: {"description": "Article Version Not Found"},
    },
    tags=["v2/public"],
    summary="Get ArticleVersion",
    response_model_by_alias=True,
)
async def get_article_version_by_id_v2(
    id: str = Path(..., description=""),
    lan: str = Query(None, description="Language of the ArticleVersion", alias="lan"),
) -> ArticleVersionV2:
    """Get an ArticleVersion identified by it&#39;s unique ID"""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_version_by_id_v2(id, lan)


@router.get(
    "/v2/articles/{id}/versions",
    responses={
        200: {"model": ArticleVersionListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article not Found"},
    },
    tags=["v2/public"],
    summary="Get Article&#39;s ArticleVersions",
    response_model_by_alias=True,
)
async def get_article_version_list_by_article_idv2(
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset"),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleVersionListV2:
    """Get a list of ArticleVersions of a given Article. Results can be sorted by creation date adn support pagination."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_article_version_list_by_article_idv2(id, offset, limit, order)


@router.get(
    "/v2/articles/commented_by/{id}",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, inavalid User ID format"},
        404: {"description": "User Not Found"},
    },
    tags=["v2/public"],
    summary="Get Articles commented by User",
    response_model_by_alias=True,
)
async def get_articles_commented_by_user_v2(
    id: str = Path(..., description=""),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query(None, description="Sorts the articles by different criteria", alias="order"),
) -> ArticleListV2:
    """Get a list of the Articles commented by a given user."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseV2PublicApi.subclasses[0]().get_articles_commented_by_user_v2(id, offset, limit, order)


@router.get(
    "/v2/articles",
    responses={
        200: {"model": ArticleListV2, "description": "OK"},
        400: {"description": "Bad Request, invalid input paramaters"},
        404: {"description": "Article Not Found"},
    },
    tags=["v2/public"],
    summary="Search for Articles",
    response_model_by_alias=True,
)
async def search_articles_v2(
    wiki_id: str = Query(None, description="The ID of the wiki where the serch will be made", alias="wiki_id"),
    name: str = Query(None, description="Search query for the name of the article", alias="name"),
    tags: list[str] = Query(None, description="A comma-separated list of tag IDs to search for", alias="tags"),
    offset: int = Query(0, description="The index of the first result to return. Use with limit to get the next page of search results.", alias="offset", ge=0),
    limit: int = Query(20, description="The maximum number of results to return.", alias="limit", ge=0, le=100),
    order: str = Query('none', description="Sorts the articles by different criteria", alias="order"),
    creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
    author_name: str = Query(None, description="Filter for the author of the Article", alias="author_name"),
    editor_name: str = Query(None, description="Filter for the editors of the Article", alias="editor_name"),
    lan: str = Query(None, description="Language of the ArticleVersion, original language if not specified", alias="lan")
) -> ArticleListV2:
    """Get a list of Articles from a given Wiki that match a keyword string. Results can by filtered by tags, sorted by different parameters and support pagination."""
    if not BaseV2PublicApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseV2PublicApi.subclasses[0]().search_articles(wiki_id, name, tags, offset, limit, order, creation_date, author_name, editor_name, lan)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid input parameters.")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article Not Found")
