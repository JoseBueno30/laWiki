# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from bson.errors import InvalidId

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
from openapi_server.models.comment import Comment
from openapi_server.models.comment_list_response import CommentListResponse
from openapi_server.models.new_comment import NewComment

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/comments/{comment_id}",
    responses={
        204: {"description": "No Content, comment deleted successfully"},
        400: {"description": "Bad Request, invalid Comment ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Comment not found"},
    },
    tags=["default"],
    summary="Delete Comment",
    response_model_by_alias=True,
)
async def delete_comment(
        comment_id: str = Path(..., description="The unique ID of the article"),
) -> None:
    """Deletes an article&#39;s comment"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().delete_comment(comment_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad Request, Invalid Comment ID format")
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@router.get(
    "/comments/articles/{article_id}",
    responses={
        200: {"model": CommentListResponse, "description": "OK"},
        400: {"description": "Bad Request, invalid parameters"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get Articles Comments",
    response_model_by_alias=True,
)
async def get_article_comments(
        article_id: str = Path(..., description="The unique ID of the article"),
        order: str = Query('recent', description="Set the order the comments will be shown. It is determined by date",
                           alias="order"),
        limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
        offset: int = Query(0,
                            description="The index of the first result to return. Use with limit to get the next page of search results.",
                            alias="offset", ge=0),
        creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
) -> CommentListResponse:
    """Retrieves all comments from an articles"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().get_article_comments(article_id, order, limit, offset,
                                                                         creation_date)
    except (InvalidId,ValueError):
        raise HTTPException(status_code=400, detail="Invalid parameters")
    except Exception:
        raise HTTPException(status_code=404)

@router.get(
    "/comments/users/{user_id}",
    responses={
        200: {"model": CommentListResponse, "description": "OK"},
        400: {"description": "Bad Request, invalid User ID format"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get Users Comments",
    response_model_by_alias=True,
)
async def get_users_comments(
        user_id: str = Path(..., description="The unique ID of the user"),
        article_id: str = Query(None, description="Fillters the results by the article&#39;s ID", alias="article_id"),
        order: str = Query('recent', description="Set the order the comments will be shown. It is determined by date",
                           alias="order"),
        limit: int = Query(20, description="Maximum amount of responses to be returned", alias="limit", ge=0, le=100),
        offset: int = Query(0,
                            description="The index of the first result to return. Use with limit to get the next page of search results.",
                            alias="offet", ge=0),
        creation_date: str = Query(None, description="Single date or range", alias="creation_date"),
) -> CommentListResponse:
    """Retrieves all comments from a user"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().get_users_comments(user_id, article_id, order, limit, offset,
                                                                       creation_date)
    except (InvalidId,ValueError):
        raise HTTPException(status_code=400, detail="Bad Request, invalid parameters")
    except Exception:
        raise HTTPException(status_code=404)


@router.post(
    "/comments/articles/{article_id}",
    responses={
        201: {"model": Comment, "description": "Comment successufully created"},
        400: {"description": "Bad Request, wrong content structure"},
        403: {"description": "Forbidden"},
        404: {"description": "Article or Author not found"},
    },
    tags=["default"],
    summary="Post Comment",
    response_model_by_alias=True,
)
async def post_comment(
        article_id: str = Path(..., description="The unique ID of the article"),
        new_comment: NewComment = Body(None,
                                       description="JSON object that contains the author and content of the comment"),
) -> Comment:
    """Posts a new comment in an article"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    try:
        return await BaseDefaultApi.subclasses[0]().post_comment(article_id, new_comment)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Bad Request, wrong content structure")
    except Exception as e:
        if e.args:
            raise HTTPException(status_code=404, detail=e.args[0])
        else:
            raise HTTPException(status_code=404, detail="Article or Author not found")
