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
from openapi_server.models.average_rating import AverageRating
from openapi_server.models.new_rating import NewRating
from openapi_server.models.rating import Rating


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/ratings/{id}",
    responses={
        204: {"description": "Deleted successfully"},
        400: {"description": "Bad Request, invalid Rating ID format"},
        403: {"description": "No permissions to delete"},
        404: {"description": "Rating Not Found"},
    },
    tags=["default"],
    summary="Delete Rating",
    response_model_by_alias=True,
)
async def delete_rating(
    id: str = Path(..., description=""),
) -> None:
    """Delete the rating associated with the selected ID"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().delete_rating(id)


@router.put(
    "/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Rating edited"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Edit Article&#39;s Rating",
    response_model_by_alias=True,
)
async def edit_article_rating(
    id: str = Path(..., description=""),
    rating: Rating = Body(None, description=""),
) -> Rating:
    """Update the value of an already existing Rating"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().edit_article_rating(id, rating)


@router.get(
    "/ratings/articles/{id}/average",
    responses={
        200: {"model": AverageRating, "description": "OK"},
        400: {"description": "Bad Request, invalid Article ID format"},
    },
    tags=["default"],
    summary="Get Article&#39;s average rating",
    response_model_by_alias=True,
)
async def get_article_average_rating(
    id: str = Path(..., description=""),
) -> AverageRating:
    """Get data about the average rating of the article"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_article_average_rating(id)


@router.get(
    "/ratings/{id}",
    responses={
        200: {"model": Rating, "description": "Rating found and returned"},
        400: {"description": "Bad Request, invalid Rating ID format"},
        404: {"description": "Rating Not Found"},
    },
    tags=["default"],
    summary="Get Rating",
    response_model_by_alias=True,
)
async def get_rating(
    id: str = Path(..., description=""),
) -> Rating:
    """Get the Rating with the provided ID"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_rating(id)


@router.get(
    "/ratings/articles/{articleId}/users/{userId}",
    responses={
        200: {"model": Rating, "description": "OK"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity (WebDAV)"},
    },
    tags=["default"],
    summary="Your GET endpoint",
    response_model_by_alias=True,
)
async def get_ratings_articles_id_users_id(
    articleId: str = Path(..., description=""),
    userId: str = Path(..., description=""),
) -> Rating:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_articles_id_users_id(articleId, userId)


@router.get(
    "/ratings/wikis/{id}",
    responses={
        200: {"model": float, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get Wiki rating",
    response_model_by_alias=True,
)
async def get_ratings_wikis_id(
    id: str = Path(..., description=""),
) -> float:
    """Get the average rating of a Wiki based on the Ratings of the Articles it has"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_ratings_wikis_id(id)


@router.get(
    "/ratings/users/{id}",
    responses={
        200: {"model": float, "description": "Return the user rating"},
        400: {"description": "Bad Request, invalid User ID format"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Get User rating",
    response_model_by_alias=True,
)
async def get_user_rating(
    id: str = Path(..., description=""),
) -> float:
    """Get the average rating of an User based on the Ratings of the Articles he made"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_user_rating(id)


@router.post(
    "/ratings/articles/{id}",
    responses={
        201: {"model": Rating, "description": "Rating created"},
        400: {"description": "Bad Request, invalid Article ID format"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Rate Article",
    response_model_by_alias=True,
)
async def rate_article(
    id: str = Path(..., description=""),
    new_rating: NewRating = Body(None, description=""),
) -> Rating:
    """Create a rating for a given Article"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().rate_article(id, new_rating)
