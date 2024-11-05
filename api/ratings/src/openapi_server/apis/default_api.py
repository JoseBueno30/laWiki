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
from openapi_server.models.inline_response200 import InlineResponse200
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating
from openapi_server.models.rating_list import RatingList


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/ratings/{id}",
    responses={
        204: {"description": "Deleted successfully"},
        403: {"description": "No permissions to delete"},
        404: {"description": "Rating Not Found"},
    },
    tags=["default"],
    summary="Delete rating by ID",
    response_model_by_alias=True,
)
async def delete_ratings_id(
    id: str = Path(..., description=""),
) -> None:
    """Delete the rating associated with the selected ID"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().delete_ratings_id(id)


@router.get(
    "/ratings/articles/{id}",
    responses={
        200: {"model": RatingList, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get all ratings of an article",
    response_model_by_alias=True,
)
async def get_ratings_article_id(
    id: str = Path(..., description=""),
    order: str = Query(None, description="", alias="order"),
    limit: int = Query(None, description="", alias="limit"),
    offset: int = Query(None, description="", alias="offset"),
) -> RatingList:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_article_id(id, order, limit, offset)


@router.get(
    "/ratings/articles/{id}/average",
    responses={
        200: {"model": InlineResponse200, "description": "OK"},
    },
    tags=["default"],
    summary="Get average rating on selected Article",
    response_model_by_alias=True,
)
async def get_ratings_article_id_average(
    id: str = Path(..., description=""),
) -> InlineResponse200:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_article_id_average(id)


@router.get(
    "/ratings/{id}",
    responses={
        200: {"model": Rating, "description": "Rating found and returned"},
        404: {"description": "Rating Not Found"},
    },
    tags=["default"],
    summary="Get rating by ID",
    response_model_by_alias=True,
)
async def get_ratings_id(
    id: str = Path(..., description=""),
) -> Rating:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_id(id)


@router.get(
    "/ratings/users/{id}",
    responses={
        200: {"model": float, "description": "Return the user rating"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get the rating from an user",
    response_model_by_alias=True,
)
async def get_ratings_user_id(
    id: str = Path(..., description=""),
) -> float:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_user_id(id)


@router.post(
    "/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Create a new rating related with an article, this MUST change the author&#39;s rating"},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Create rating on article",
    response_model_by_alias=True,
)
async def post_ratings_article_id(
    id: str = Path(..., description=""),
    new_rating: NewRating = Body(None, description=""),
) -> Rating:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_ratings_article_id(id, new_rating)


@router.put(
    "/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Edited rating"},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Edit rating of an article",
    response_model_by_alias=True,
)
async def put_ratings_article_id(
    id: str = Path(..., description=""),
    rating: Rating = Body(None, description=""),
) -> Rating:
    """This endpoint must do the same as Post but editting the value instead of creating a new one"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().put_ratings_article_id(id, rating)
